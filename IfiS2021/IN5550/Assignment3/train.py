import os
import argparse
import time
import json
import numpy as np
from typing import Any, Dict
import torch
from config import NORBERT_HUGGINGFACE_PATH
import tqdm
from conllu import parse
from torch import nn
from dataset import NERdata
from model import NERmodel
from transformers import AdamW
from transformers import BertTokenizer
from torch.utils.data import DataLoader
from data_utils import collate_fn, build_mask
from torch.utils.tensorboard import SummaryWriter


DEFAULT_CONFIG = {
    "train_path": "./data/train.conllu",
    "dev_path": "./data/dev.conllu",
    "seed": 420,
    "epochs": 20,
    "lr": 1e-3,
    "batch_size": 8,
    "model_folder": "./classifiers/",
    "check_n_iterations": 1000,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--train_data_path", type=str, default=DEFAULT_CONFIG["train_path"],
                        help="The path where the train dataset lies")

    parser.add_argument("--dev_set", type=str, default=DEFAULT_CONFIG["dev_path"],
                        help="Path to a dev set which is user to measure validation loss")

    parser.add_argument("--seed", type=int, default=DEFAULT_CONFIG["seed"],
                        help="Seed for reproducibility")

    parser.add_argument("--config", help="path of json file for configuration")

    args = parser.parse_args()

    return args


def train_model(train_dataset, val_dataset,
                config: Dict[str, Any]) -> nn.Module:
    """
    Trains model and checkpoints on best validation loss
    """
    epochs = config["epochs"]
    model_folder = config["model_folder"]
    check_n_iterations = config["check_n_iterations"]
    batch_size = config["batch_size"]
    lr = config["lr"]
    writer = SummaryWriter(f"classifier_logs")

    train_time_sum = 0

    vocab_size = len(train_dataset.label_vocab)

    model = NERmodel(vocab_size)
    tokenizer = BertTokenizer.from_pretrained(
        NORBERT_HUGGINGFACE_PATH, do_basic_tokenize=False)
    criterion = nn.CrossEntropyLoss(ignore_index=-1)
    optimizer = AdamW(model.parameters(), lr=lr)

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, collate_fn=collate_fn, shuffle=True)
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, collate_fn=collate_fn, shuffle=False)

    def save_checkpoint(file_name):
        torch.save({
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "epoch": epoch,
            "train_time_sum": train_time_sum,
        }, file_name)
        print(f"Saved model to {file_name}")

    def estimate_loss(X, y):
        with torch.no_grad():
            X = tokenizer(X, is_split_into_words=True,
                          return_tensors='pt', padding=True)['input_ids']
            batch_mask = build_mask(tokenizer, X)
            y_prime = model(X, batch_mask).permute(0, 2, 1)
            loss = criterion(y_prime, y.squeeze())
        return loss

    finished_epochs = 0
    n_batches = (len(train_dataset)//batch_size)+1
    for epoch in range(epochs):
        start_epoch_time = time.time()
        train_loss_sum = 0.0

        running_train_loss = 0.
        best_val_loss = 0.

        model.train()
        for i, (X, y) in enumerate(tqdm.tqdm(train_loader)):
            n_samples_so_far = (i*batch_size)
            optimizer.zero_grad()

            X = tokenizer(X, is_split_into_words=True,
                          return_tensors='pt', padding=True)['input_ids']

            batch_mask = build_mask(tokenizer, X)

            y_prime = model(X, batch_mask).permute(0, 2, 1)
            loss = criterion(y_prime, y.squeeze())

            loss.backward()
            optimizer.step()
            running_train_loss += loss.item()

            if (n_samples_so_far % check_n_iterations) == 0:
                print(f"[{n_samples_so_far}/{len(train_loader)*batch_size}]")
                print("current train loss:", running_train_loss)
                train_loss_sum += running_train_loss
                running_train_loss = 0.

                val_loss = get_val_loss(
                    model, tokenizer, val_loader, criterion)

                if val_loss > best_val_loss:
                    print("Saving checkpoint!")
                    best_val_loss = val_loss
                    save_checkpoint(os.path.join(
                        model_folder, "best_model.pt"))

        end_epoch_time = time.time()
        epoch_time = end_epoch_time - start_epoch_time
        train_time_sum += epoch_time

        val_loss_sum = get_val_loss(model, tokenizer, val_loader, criterion)

        n_iterations = n_batches+1
        epoch_val_loss = val_loss_sum/n_iterations
        writer.add_scalar("validation loss", epoch_val_loss, epoch)
        writer.add_scalar("validation_loss over time",
                          epoch_val_loss, train_time_sum)

        n_iterations = n_batches+1
        epoch_train_loss = train_loss_sum/n_iterations
        writer.add_scalar("training loss", epoch_train_loss, epoch)
        writer.add_scalar("training loss over time",
                          epoch_train_loss, train_time_sum)

        finished_epochs += 1

        print(
            f"epoch: {epoch}; train loss: {running_train_loss}; val loss: {val_loss_sum}; time: {epoch_time}")

    print(
        f"Finished training {finished_epochs} epochs. Total time: {train_time_sum}")
    save_checkpoint(f"{model_folder}_epoch{finished_epochs}.pt")
    writer.close()

    return model


def get_val_loss(model, tokenizer, val_loader, criterion) -> float:
    model.eval()
    val_loss_sum = 0.
    for X, y in val_loader:
        with torch.no_grad():
            X = tokenizer(X, is_split_into_words=True,
                          return_tensors='pt', padding=True)['input_ids']
            batch_mask = build_mask(tokenizer, X)
            y_prime = model(X, batch_mask).permute(0, 2, 1)
            val_loss = criterion(y_prime, y.squeeze())
            val_loss_sum += val_loss.item()

    return val_loss_sum


def set_random_seeds(seed: int) -> None:
    "Sets the global RNG seeds for reproducibility purposes"
    np.random.seed(seed)
    torch.manual_seed(seed)


def main(config: Dict[str, Any]) -> None:

    with open(config["train_data_path"], "r") as f:
        train_data_str = f.read()
    # Create Dataset objects
    train_dataset = NERdata(parse(train_data_str))

    with open(config["dev_set"], "r") as f:
        dev_data_str = f.read()

    val_dataset = NERdata(parse(dev_data_str),
                          label_vocab=train_dataset.label_vocab)

    train_model(train_dataset, val_dataset, config)


if __name__ == "__main__":
    args = parse_args()

    config = DEFAULT_CONFIG
    config.update(vars(args))

    if args.config:
        with open(args.config, "r") as f:
            config.update(json.load(f))

    seed = config["seed"]

    print("Running with random seed:", seed)
    set_random_seeds(seed)
    main(config)
