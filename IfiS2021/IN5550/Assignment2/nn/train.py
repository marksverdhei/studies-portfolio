import os
import argparse
import time
import json

import numpy as np
from typing import Any, Dict, Tuple
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

import torch
from torch import nn
from torch import optim
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.tensorboard import SummaryWriter

from data_utils import load_and_pepare_data
from data_utils import get_model_from_folder
from data_utils import batched_sampler

from models import make_classifier


DEFAULT_DATA_PATH = "data/stanford_sentiment_binary.tsv.gz"
DEFAULT_CLASSIFIER_TYPE = "linear"
DEFAULT_EMBEDDING_TYPE = "word2vec"

DEFAULT_SEED = 420
DEFAULT_MAX_FEATURES = 5000
DEFAULT_EPOCHS = 2
MODEL_FILENAME = "model"

DEFAULT_LR = 1e-3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("model_folder", type=str, nargs="?", default=None,
                        help="A given folder where the model will be saved")

    parser.add_argument("--config", type=str,
                        help="Path to a JSON file containing ")

    parser.add_argument("--train_data_path", type=str, default=DEFAULT_DATA_PATH,
                        help="The path where the train dataset lies")

    parser.add_argument("--dev_set", type=str, default=None,
                        help="Path to a dev set which is user to measure validation loss")

    parser.add_argument("--inputmethod", type=str, default=None)

    parser.add_argument("--checkpoint_on_epochs", type=int, default=5)

    parser.add_argument("--use_latest_checkpoint", action="store_true")

    # MODEL PARAMETERS
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="Seed for reproducibility")

    parser.add_argument("--model_type", type=str,
                        default=DEFAULT_CLASSIFIER_TYPE,
                        help="linear, dense, rnn, cnn, gru")

    parser.add_argument("--embedding_type", type=str,
                        default=DEFAULT_EMBEDDING_TYPE,
                        help="word2vec, fasttext or bert")

    parser.add_argument("--batch_size", type=int, default=64)

    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS,
                        help="Number of epochs to train the model")

    parser.add_argument("--learning_rate", type=float, default=DEFAULT_LR,
                        help="learning rate for the adam optimizer")

    parser.add_argument("--preprocessing", type=str, default="raw",
                        help="raw, lemmatized or pos tagged")

    # parser.add_argument("--hidden_layers", type=int, default=None)

    args = parser.parse_args()
    if args.config:
        print("Loading config", args.config)
        with open(args.config) as f:
            vars(args).update(json.load(f))

    if not args.model_folder:
        parser.error(
            "You must supply path to the model either by CLI or config")

    return args


def train_model(X_train: np.ndarray, y_train: torch.Tensor,
                epochs: int, config: Dict[str, Any]) -> nn.Module:
    """
    This function instantiates or loads a model and trains it on the supplied
    training set for the given number of epochs, then saves the model and returns
    a trained pytorch model. It requires a training config with a set number of parameters

    Loss and duration is written to a tensorboard summary writer so it can be
    inspected in tensorboard after training. Optionally, one can supply a validation
    set, so the validation loss is tracked as well.

    Through training, the model can be repeatedly saved or 'checkpointed', and the
    rate can be configured by setting checkpoint_on_epochs.
    """
    model_type = config["model_type"]
    model_path = config["model_path"]
    embedding_type = config["embedding_type"]

    preprocessing = config.get("preprocessing", "raw")
    val_set = config.get("val_set", None)
    learning_rate = config.get("learning_rate", DEFAULT_LR)
    batch_size = config.get("batch_size", 64)
    checkpoint = config.get("checkpoint", None)
    checkpoint_on_epochs = config.get("checkpoint_on_epochs", 25)

    data_size = X_train.size
    writer = SummaryWriter(f"{model_path}_logs")

    starting_epoch = 0
    train_time_sum = 0

    # model_optionals = {"raw", "preprocessing", "inputmethod", "hidden_layers"}
    # model_kwargs = {k: v for k, v in config.items() if k in model_optionals}

    model = make_classifier(**config)
    print("Created model:", model, sep="\n")

    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    if checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        starting_epoch = checkpoint["epoch"]

    model.train()
    criterion = nn.BCELoss()
    ending_epoch = starting_epoch + epochs

    cp_config_fields = {"model_type", "embedding_type",
                        "preprocessing", "inputmethod"}

    def save_checkpoint(file_name):
        torch.save({
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "epoch": epoch,
            "train_time_sum": train_time_sum,
            "config": {k: v for k, v in config.items() if k in cp_config_fields}
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

    n_batches = (data_size//batch_size)+1

    for epoch in range(starting_epoch+1, ending_epoch+1):
        start_epoch_time = time.time()

        train_loss_sum = 0.0

        for inputs, labels in batched_sampler(X_train, y_train, batch_size):
            optimizer.zero_grad()
            outputs = model(inputs)

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss_sum += loss.item()

        end_epoch_time = time.time()
        epoch_time = end_epoch_time - start_epoch_time
        n_iterations = n_batches+1

        train_time_sum += epoch_time

        epoch_train_loss = train_loss_sum/n_iterations
        print(f"\n[Epoch {epoch}] training loss: {epoch_train_loss}")
        writer.add_scalar("training loss", epoch_train_loss, epoch)
        writer.add_scalar("training loss over time",
                          epoch_train_loss, train_time_sum)

        if val_set is not None:
            X_val, y_val = val_set
            epoch_val_loss = estimate_loss(X_val, y_val)
            print(f"validation loss: {epoch_val_loss}")
            writer.add_scalar("validation loss", epoch_val_loss, epoch)
            writer.add_scalar("validation_loss over time",
                              epoch_val_loss, train_time_sum)

        print("Finished epoch", epoch, "in", epoch_time, "seconds")
        writer.add_scalar("epoch_time", epoch_time, epoch)

        if not (epoch % checkpoint_on_epochs):
            save_checkpoint(f"{model_path}_epoch{epoch}.pt")

    print("Finished Training at", epoch, "epochs in", train_time_sum, "seconds")
    save_checkpoint(f"{model_path}_epoch{epoch}.pt")
    writer.close()

    return model


def set_random_seeds(seed: int) -> None:
    "Sets the global RNG seeds for reproducibility purposes"
    np.random.seed(seed)
    torch.manual_seed(seed)


def main(args: argparse.Namespace) -> None:

    # set path variables
    model_folder_path = args.model_folder
    model_path = f"{model_folder_path}/{MODEL_FILENAME}"

    load = os.path.exists(model_folder_path)

    if load:
        print("Found path", model_folder_path)
    else:
        print("Path not found, creating new directory...")
        os.mkdir(model_folder_path)

    # -------- Initiate preprocessing ------
    dir_list = os.listdir(model_folder_path)

    # -------- Load dataset ---------------

    # X_train is numpy array of text sentences, y_train is binary encoded labels

    X_train, y_train = load_and_pepare_data(
        args.train_data_path, preprocessing=args.preprocessing)

    dev_set = None
    if args.dev_set is not None:
        dev_set = X_dev, y_dev = load_and_pepare_data(
            args.dev_set, preprocessing=args.preprocessing)

    # -------- Initiate classifier model --------
    # Load or create model
    checkpoint = None

    if load:
        print("Found directory", model_folder_path)
        print("Loading objects")
        selected_model_path = get_model_from_folder(
            model_folder_path, args.use_latest_checkpoint)

        if selected_model_path is not None:
            checkpoint = torch.load(
                f"{model_folder_path}/{selected_model_path}")

    if checkpoint is None:
        print("Creating new model")

    print("Checpointing every", args.checkpoint_on_epochs, "epochs")

    arg_dict = vars(args)
    arg_dict.update({
        "model_path": model_path,
        "val_set": dev_set,
        "checkpoint": checkpoint,
    })
    # ------ TRAIN ----
    train_model(
        X_train,
        y_train,
        args.epochs,
        arg_dict
    )


if __name__ == "__main__":
    args = parse_args()

    print("Running with random seed:", args.seed)
    set_random_seeds(args.seed)
    main(args)
