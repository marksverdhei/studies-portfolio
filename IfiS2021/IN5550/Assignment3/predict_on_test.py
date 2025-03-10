import argparse
import torch
from conllu import parse
import pandas as pd
from sklearn import metrics
from dataset import NERdata
from torch.utils.data import DataLoader
from data_utils import build_mask, collate_fn
from model import NERmodel
from transformers import BertTokenizer


DEFAULT_DEST = "./predictions.conllu"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_path", type=str, default="data/dev.conllu",
                        help="The path to the test set")

    parser.add_argument("--model", type=str, default=None,
                        help="Path to the pytorch model in .pt format")

    parser.add_argument("--dest", type=str, default="predictions.tsv",
                        help="Path to the destination")

    parser.add_argument("--tagged", action="store_true")

    return parser.parse_args()


def get_predictions():
    pass

def get_targets(testloader):
    return torch.vstack([y for _, y in testloader])


def main(args):
    if args.model:
        model_data = torch.load(args.model)
        model_config = model_data["config"]

    with open(args.test_path, "r") as f:
        data_str = f.read()

    test_dataset = NERdata(parse(data_str))

    test_loader = DataLoader(test_dataset, collate_fn=collate_fn, batch_size=128, shuffle=False)

    tokenizer = BertTokenizer.from_pretrained('ltgoslo/norbert')

    # LOAD MODEL
    model = NERmodel(len(test_dataset.label_vocab))

    model.eval()

    def predict_fn(X):
        tokens = tokenizer(X, is_split_into_words=True, return_tensors='pt', padding=True)['input_ids']
        batch_mask = build_mask(tokenizer, X)
        y_prime = model(X, batch_mask).permute(0, 2, 1).argmax(1)
        return y_prime

    with torch.no_grad():
        predictions = [predict_fn(X) for X, _ in tqdm(testloader)]

    print(predictions)

    # with open(DEFAULT_DEST, "w+") as outfile:
    #     outfile.write(conllu_str)


if __name__ == "__main__":
    args = parse_args()
    main(args)
