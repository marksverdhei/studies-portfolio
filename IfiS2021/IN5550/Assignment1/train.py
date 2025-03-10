import os
import argparse
import time
import numpy as np
from typing import Any, Dict, Tuple
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

import torch
from torch import nn
from torch import optim
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.tensorboard import SummaryWriter

from data_utils import load_signal_data, csr_to_float_tensor
from data_utils import pickle_objects, unpickle_objects
from data_utils import get_model_from_folder
from model import DenseNeuralClassifier

DEFAULT_DATA_PATH = "data/signal_20_obligatory1_train.tsv"
DEFAULT_SEED = 420
DEFAULT_MAX_FEATURES = 5000
DEFAULT_EPOCHS = 2
DEFAULT_VECTORIZER = "count"

MODEL_FILENAME = "model"
FE_FILENAME = "feature_encoder.pickle"
LE_FILENAME = "label_encoder.pickle"

DEFAULT_LR = 1e-3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("train_data_path", type=str, default=DEFAULT_DATA_PATH,
                        help="The path where the train dataset lies")

    parser.add_argument("model_folder", type=str,
                        help="A given folder where the model will be saved along with"
                             "feature and label encoders")

    parser.add_argument("--dev_set", type=str, default=None,
                        help="Path to a dev set which is user to measure validation loss")

    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="Seed for reproducibility")

    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS,
                        help="Number of epochs to train the model")

    parser.add_argument("--max_features", type=int, default=DEFAULT_MAX_FEATURES,
                        help="The maximum amount of unique words to encode")

    parser.add_argument("--vectorizer", type=str, default=DEFAULT_VECTORIZER,
                        help="Type of BOW vectorizer: (count | binary | tfidf), default=count")

    parser.add_argument("--learning_rate", type=float, default=DEFAULT_LR,
                        help="learning rate for the adam optimizer")

    parser.add_argument("--sparse_tensor", action="store_true")

    parser.add_argument("--batch_size", type=int, default=64)

    parser.add_argument("--checkpoint_on_epochs", type=int, default=5)

    parser.add_argument("--hidden_layers", type=int, default=None)

    parser.add_argument("--use_latest_checkpoint", action="store_true")


    return parser.parse_args()


def train_model(
        # Positional, required arguments:
        X_train: torch.Tensor,
        y_train: torch.Tensor,
        epochs: int,
        model_path: str,
        # Optional, keyword arguments:
        val_set: Tuple[torch.Tensor, torch.Tensor] = None,
        learning_rate: float = DEFAULT_LR,
        batch_size: int = 64,
        checkpoint: Dict[str, Any] = None,
        checkpoint_on_n_epochs: int = 25,
        hidden_layers: int = None,
        ) -> nn.Module:
    """
    This function initates or loads a model and trains it on the supplied
    training set for the given number of epochs, then saves the model and returns
    a trained pytorch model.

    Loss and duration is written to a tensorboard summary writer so it can be
    inspected in tensorboard after training. Optionally, one can supply a validation
    set, so the validation loss is tracked as well.

    Through training, the model can be repeatedly saved or 'checkpointed', and the
    rate can be configured by setting checkpoint_on_n_epochs.
    """


    n_features = X_train.shape[-1]
    n_classes = len(y_train.unique())

    writer = SummaryWriter(f"{model_path}_logs")

    starting_epoch = 0
    train_time_sum = 0

    if checkpoint:
        starting_epoch = checkpoint.get("epoch", 0)
        train_time_sum = checkpoint.get("train_time_sum", 0)

        hl_checkpoint = checkpoint.get("hidden_layers", 2)
        assert (hl_checkpoint == hidden_layers or hidden_layers is None), f"Mismatch with hidden layer argument and checkpoint (a:{hidden_layers}, c:{hl_checkpoint})"
        hidden_layers = hl_checkpoint
    elif hidden_layers is None:
        hidden_layers = 2

    model = DenseNeuralClassifier(n_features, n_classes, hidden_layers=hidden_layers)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    if checkpoint:
        try:
            model.load_state_dict(checkpoint["model_state_dict"])
            optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        except RuntimeError as e:
            print(e)
            print("***\nError loading state dict. Try to change model folder path")
            
    model.train()

    criterion = nn.CrossEntropyLoss()

    tensor_dataset = TensorDataset(X_train, y_train)
    trainloader = DataLoader(tensor_dataset, batch_size=batch_size)
    ending_epoch = starting_epoch + epochs


    def save_checkpoint(file_name):
        torch.save({
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "epoch": epoch,
            "hidden_layers": hidden_layers,
            "train_time_sum": train_time_sum
        }, file_name)
        print(f"Saved model to {file_name}")

    def estimate_loss(X, y):
        with torch.no_grad():
            y_prime = model(X)
            loss = criterion(y_prime, y)
        return loss

    initial_train_loss = estimate_loss(X_train, y_train)
    print(f"\n[Epoch {starting_epoch}] mean loss: {initial_train_loss}")
    writer.add_scalar("training loss", initial_train_loss, starting_epoch)


    if val_set is not None:
        X_val, y_val = val_set
        initial_val_loss = estimate_loss(X_val, y_val)
        print(f"validation loss: {initial_val_loss}")
        writer.add_scalar("validation loss", initial_val_loss, starting_epoch)


    for epoch in range(starting_epoch+1, ending_epoch+1):
        start_epoch_time = time.time()

        train_loss_sum = 0.0
        val_loss_sum = 0.0

        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = model(inputs)

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss_sum += loss.item()

        end_epoch_time = time.time()
        epoch_time = end_epoch_time - start_epoch_time
        n_iterations = i+1

        train_time_sum += epoch_time

        epoch_train_loss = train_loss_sum/n_iterations
        print(f"\n[Epoch {epoch}] mean loss: {epoch_train_loss}")
        writer.add_scalar("training loss", epoch_train_loss, epoch)
        writer.add_scalar("training loss over time", epoch_train_loss, train_time_sum)


        if val_set is not None:
            X_val, y_val = val_set
            epoch_val_loss = estimate_loss(X_val, y_val)
            print(f"validation loss: {epoch_val_loss}")
            writer.add_scalar("validation loss", epoch_val_loss, epoch)
            writer.add_scalar("validation_loss over time", epoch_val_loss, train_time_sum)


        print("Finished epoch", epoch, "in", epoch_time, "seconds")
        writer.add_scalar("epoch_time", epoch_time, epoch)

        if not (epoch % checkpoint_on_n_epochs):
            save_checkpoint(f"{model_path}_epoch{epoch}.pt")



    print("Finished Training at", epoch, "epochs in",
          train_time_sum, "seconds")
    save_checkpoint(f"{model_path}_epoch{epoch}.pt")

    writer.close()

    return model


def get_vectorizer(vec_type: str, max_features: int):
    "Handles supplied command line argument and returns a vectorizer with a given vocab size"
    if vec_type == "count":
        return CountVectorizer(max_features=max_features)
    elif vec_type == "binary":
        return CountVectorizer(max_features=max_features, binary=True)
    elif vec_type == "tfidf":
        return TfidfVectorizer(max_features=max_features)
    else:
        raise TypeError(f"Invalid encoder type {vec_type} pick between count, binary or tfidf")


def set_random_seeds(seed: int) -> None:
    "Sets the global RNG seeds for reproducibility purposes"
    np.random.seed(seed)
    torch.manual_seed(seed)


def main(args: argparse.Namespace) -> None:


    ## set path variables
    model_folder_path = f"models/{args.model_folder}"
    model_path = f"{model_folder_path}/{MODEL_FILENAME}"
    feature_encoder_path = f"{model_folder_path}/{FE_FILENAME}"
    label_encoder_path = f"{model_folder_path}/{LE_FILENAME}"

    load = os.path.exists(model_folder_path)

    if load:
        print("Found path", model_folder_path)
    else:
        print("Path not found, creating new directory...")
        os.mkdir(model_folder_path)

    # -------- Initiate preprocessing ------
    dir_list = os.listdir(model_folder_path)
    encoders_exist = FE_FILENAME in dir_list and LE_FILENAME in dir_list
    if encoders_exist:
        feature_encoder, label_encoder = unpickle_objects(
            feature_encoder_path, label_encoder_path
        )
    else:
        feature_encoder = get_vectorizer(args.vectorizer, args.max_features)
        label_encoder = LabelEncoder()

    # -------- Load dataset ---------------
    X_train, y_train = load_signal_data(
        args.train_data_path, feature_encoder, label_encoder,
        fit_encoders=True
    )

    if args.sparse_tensor:
        X_train_tensor = csr_to_float_tensor(X_train)
    else:
        X_train_tensor = torch.tensor(X_train.toarray(), dtype=torch.float32)

    y_train_tensor = torch.tensor(y_train)

    dev_set = None
    if args.dev_set is not None:
        X_val, y_val = load_signal_data(
            args.dev_set, feature_encoder, label_encoder,
            fit_encoders=False
        )
        X_val_tensor = torch.tensor(X_val.toarray(), dtype=torch.float32)
        y_val_tensor = torch.tensor(y_val)
        dev_set = (X_val_tensor, y_val_tensor)

    # write encoders
    if not encoders_exist:
        encoders = {
            feature_encoder_path: feature_encoder,
            label_encoder_path: label_encoder
        }
        pickle_objects(encoders, verbose=True)


    # -------- Initiate model --------
    ## Load or create model
    checkpoint = None

    if load:
        print("Found directory", model_folder_path)
        print("Loading objects")
        selected_model_path = get_model_from_folder(model_folder_path, args.use_latest_checkpoint)

        if selected_model_path is not None:
            checkpoint = torch.load(f"{model_folder_path}/{selected_model_path}")

    if checkpoint is None:
        print("Creating new model")

    print("Checpointing every", args.checkpoint_on_epochs, "epochs")

    # ------ TRAIN ----
    train_model(
        X_train_tensor,
        y_train_tensor,
        args.epochs,
        model_path,
        val_set=dev_set,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        checkpoint=checkpoint,
        checkpoint_on_n_epochs=args.checkpoint_on_epochs,
        hidden_layers=args.hidden_layers
    )


if __name__ == "__main__":
    args = parse_args()
    print("Running with random seed:", args.seed)
    set_random_seeds(args.seed)
    main(args)
