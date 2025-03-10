import torch
import random
import argparse
import numpy as np
import torch.nn.functional as F
from conllu import parse

DEFAULT_DATA_PATH = "./data/norne-nb-in5550-train.conllu"


def collate_fn(batch):
    longest_y = max([y.size(0) for X, y in batch])
    X = [X for X, y in batch]
    y = torch.stack([F.pad(y, (0, longest_y - y.size(0)), value=-1)
                     for X, y in batch])
    return X, y


def build_mask(tokenizer, ids):
    tok_sents = [tokenizer.convert_ids_to_tokens(i) for i in ids]
    mask = []
    for sentence in tok_sents:
        current = []
        for n, token in enumerate(sentence):
            if token in tokenizer.all_special_tokens or token.startswith('##'):
                if(token in ["[UNK]"]):
                    current.append(n)
                else:
                    continue
            else:
                current.append(n)
        mask.append(current)

    mask = tokenizer.pad({'input_ids': mask}, return_tensors='pt')['input_ids']
    return mask


def make_train_dev_set(
    source_path: str,
    train_path: str,
    dev_path: str,
    seed: int = None,
) -> None:
    "Saves a new train and dev set"
    print("Running with seed:", seed)
    if seed is not None:
        np.random.seed(seed)

    data = parse(open(source_path, "r").read())
    random.shuffle(data)

    train = data[:8*len(data)//10]
    dev = data[8*len(data)//10:]

    with open(train_path, 'w+') as f:
        f.writelines([s.serialize() + "\n" for s in train])

    with open(dev_path, 'w+') as f:
        f.writelines([s.serialize() + "\n" for s in dev])


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
                       args.dev_path, seed=420)
