import argparse
import torch
import pandas as pd
from sklearn import metrics

from data_utils import load_and_pepare_data
from models import make_classifier
DEFAULT_DEST = "./predictions.tsv"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_path", type=str, required=True,
                        help="The path to the test set")

    parser.add_argument("--model", type=str, required=True,
                        help="Path to the pytorch model in .pt format")

    parser.add_argument("--dest", type=str, default="predictions.tsv",
                        help="Path to the destination")

    parser.add_argument("--tagged", action="store_true")

    return parser.parse_args()


def main(args):
    model_data = torch.load(args.model)
    model_config = model_data["config"]
    X_test, y_test = load_and_pepare_data(args.test_path, model_config["preprocessing"])

    model = make_classifier(**model_config)
    model.load_state_dict(model_data["model_state_dict"])
    model.eval()

    with torch.no_grad():
        y_pred = model(X_test)

    activations = y_pred.squeeze().numpy()

    threshold = 0.5
    predictions = ["positive" if i > threshold else "negative" for i in activations]

    df = pd.DataFrame({"label": predictions})
    df.to_csv(args.dest, sep="\t", index=False)


if __name__ == "__main__":
    args = parse_args()
    main(args)
