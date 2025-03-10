import os
import re
import argparse
import pandas as pd
import numpy as np
import torch
from typing import Any, Dict, Generator, Iterable, List, Tuple, Union

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

DEFAULT_DATA_PATH = "../data/stanford_sentiment_binary.tsv.gz"


def batched_sampler(X, y, batch_size, shuffle=True):
    """
    Generator function that yields the data in batches of batch_size
    """
    size = len(X)
    if shuffle:
        perm = np.random.permutation(size)
        X = X[perm]
        y = y[perm]

    for i in range(0, size, batch_size):
        yield X[i:i+batch_size], y[i:i+batch_size]


def select_found_model(options: List[str]) -> str:
    """
    Takes in a list of possible model files and
    selects the file selected by the user using stdin, if multiple are found
    """

    if len(options) == 1:
        selected_path = options[0]
        print("Found model:", selected_path)
        return selected_path

    elif len(options) > 1:
        print("Found multiple models:")
        print("\n".join(f"{i}: {fn}" for i, fn in enumerate(options)))

        while True:
            ans = input("Select file: ")
            if ans.isdigit():
                idx = int(ans)
                if 0 <= idx < len(options):
                    return options[idx]

            print("Invalid input. ", end="")
    else:
        print("No model with extension .pt in given folder")
        return None


def get_model_from_folder(path: str, use_latest_checkpoint: bool = False) -> str:
    """
    Returns None if no found model, str otherwise. If multiple are found, it prompts
    the user to select from stdin, unless 'use_latest_checkpoint' is set to True
    """
    options = [s for s in os.listdir(path) if s.endswith(".pt")]
    if use_latest_checkpoint:
        def get_epoch_number(x): return int(re.sub('[^0-9]', '', x))
        if options:
            options = [max(options, key=get_epoch_number)]

    return select_found_model(options)


def load_and_pepare_data(data_path: str, preprocessing="pos_lemma") -> Tuple[np.ndarray, np.ndarray]:
    "Returns a numpy array of sentences and the corresponding labels"
    data = pd.read_csv(data_path, sep="\t")
    labels, raw_text, lemma_pos_text = data.to_numpy().T

    if(preprocessing == "lemmatized"):
        X = lemma_pos_text

        for index, row in enumerate(X):
            X[index] = re.sub(r"\_.*?(\s|$)", " ", row)

    if (preprocessing == "pos_lemma"):
        X = lemma_pos_text

    if (preprocessing == "raw"):
        X = raw_text

    '''

    if preprocessing == "raw":
        X = raw_text
    elif "lemma" in preprocessing and "pos" in preprocessing:
        X = lemma_pos_text
    else:
        lemma_tag = (s.split("_") for s in lemma_pos_text)
        if preprocessing == "pos_tagged":
            X = np.array([f"{word}_{tag}" for word,
                          (lemma, tag) in zip(raw_text, lemma_tag)])
        elif preprocessing == "lemmatized":

            X = np.array([lemma for lemma, tag in lemma_tag])
        else:
            raise TypeError("Passed invalid preprocessing argument")

    '''

    labels_encoded = (labels == "positive").astype(int)
    y = torch.tensor(labels_encoded, dtype=torch.float32).unsqueeze(1)
    print(X[0:10])
    return X, y


def make_train_dev_set(
    source_path: str,
    train_path: str,
    dev_path: str,
    dev_size: float = 0.3,
    seed: int = None,
    frac: float = 1,
    max_size: float = float("inf")


) -> None:
    "Saves a new train and dev set to a tsv file on the same format of signal_20_obligatory1_train"
    print("Running with seed:", seed)
    if seed is not None:
        np.random.seed(seed)

    df = pd.read_csv(source_path, sep="\t")
    df_shuffeled = df.sample(frac=frac)
    size = int(min(max_size, len(df)))

    data = df_shuffeled[:size]
    train, dev = train_test_split(data, test_size=dev_size)

    train.to_csv(train_path, sep="\t", index=False)
    dev.to_csv(dev_path, sep="\t", index=False)
    print("Successfully created train and dev set with ratios", 1-dev_size, dev_size)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("train_path", type=str,
                    help="The path to leave the new train set")
    ap.add_argument("dev_path", type=str,
                    help="The path to leave the new test set")
    ap.add_argument("--source_path", type=str,
                    default=DEFAULT_DATA_PATH, help="source tsv")
    ap.add_argument("--frac", type=float, default=1,
                    help="fraction of the original data")
    args = ap.parse_args()
    # We fix the seed for reproducibility
    make_train_dev_set(args.source_path, args.train_path,
                       args.dev_path, seed=420, frac=args.frac)
