import os
import re
import argparse
import pandas as pd
import numpy as np
import torch
import scipy
import pickle
from typing import Any, Dict, Generator, Iterable, List, Tuple, Union

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

SIGNAL_DATA_PATH = "data/signal_20_obligatory1_train.tsv"

def csr_to_float_tensor(csr_matrix: scipy.sparse.csr_matrix) -> torch.sparse.FloatTensor:
    "Transforms a scipy tensor into a torch tensor that uses coo compression"
    coo_matrix = csr_matrix.tocoo()
    values = coo_matrix.data
    indices = np.vstack((coo_matrix.row, coo_matrix.col))

    i = torch.LongTensor(indices)
    v = torch.FloatTensor(values)
    shape = coo_matrix.shape

    sparse_tt = torch.sparse.FloatTensor(i, v, torch.Size(shape))
    return sparse_tt


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
        get_epoch_number = lambda x: int(re.sub('[^0-9]','', x))
        if options:
            options = [max(options, key=get_epoch_number)]

    return select_found_model(options)


def pickle_objects(object_dict: Dict[str, Any], verbose: bool = False) -> None:
    "Takes in a dictionary of file names and python objects and serializes them"
    for path, obj in object_dict.items():
        with open(path, "wb+") as f:
            pickle.dump(obj, f)
        if verbose:
            print("Wrote object of type", type(obj), "to", path)


def unpickle_objects(*paths: List[str]) -> Generator[Any, None, None]:
    "Takes in an arbitrary number of filenames and yields them with pickle"
    for path in paths:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        yield obj


def load_signal_data(data_path: str,
                     feature_encoder: Union[CountVectorizer, TfidfVectorizer],
                     label_encoder: LabelEncoder,
                     fit_encoders: bool = True
                     ) -> Tuple[scipy.sparse.csr_matrix, np.ndarray]:
    """
    Loads the supplied data file and transforms the data using the supplied
    encoders. Calls fit_transform if 'fit_encoders' is set to true.
    Returns output of the transformation function
    """
    df = pd.read_csv(data_path, sep="\t")
    labels, features = df.values.T

    if fit_encoders:
        feature_encoder.fit(features)
        label_encoder.fit(labels)

    feature_matrix = feature_encoder.transform(features)
    label_vector = label_encoder.transform(labels)

    return feature_matrix, label_vector


def make_train_dev_set(
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

    df = pd.read_csv(SIGNAL_DATA_PATH, sep="\t")
    df_shuffeled = df.sample(frac=frac)
    size = int(min(max_size, len(df)))

    data = df_shuffeled[:size]
    train, dev = train_test_split(data, test_size=dev_size)

    train.to_csv(train_path, sep="\t", index=False)
    dev.to_csv(dev_path, sep="\t", index=False)
    print("Successfully created train and dev set with ratios", 1-dev_size, dev_size)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("train_path", type=str, help="The path to leave the new train set")
    ap.add_argument("dev_path", type=str, help="The path to leave the new test set")
    ap.add_argument("--frac", type=float, default=1, help="fraction of the original data")
    args = ap.parse_args()
    # We fix the seed for reproducibility
    make_train_dev_set(args.train_path, args.dev_path, seed=420, frac=args.frac)
