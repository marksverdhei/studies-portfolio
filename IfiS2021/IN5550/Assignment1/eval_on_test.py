import argparse
import torch
import pandas as pd
from sklearn import metrics
from data_utils import load_signal_data, csr_to_float_tensor
from data_utils import unpickle_objects, get_model_from_folder

from model import DenseNeuralClassifier


VECTORIZER_FILE = "feature_encoder.pickle"
LABEL_ENCODER_FILE = "label_encoder.pickle"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_set_path",
                        type=str, help="The path to the test set")

    parser.add_argument("model_folder", type=str,
                        help="The folders where the models and encoders are found")

    parser.add_argument("--as_markdown", action="store_true")

    parser.add_argument("--use_latest_checkpoint", action="store_true")

    return parser.parse_args()


def predict_classes(X, model):
    "Returns an array of predicted classes on the form of the label array"
    y_dists = model(X)
    y_pred = torch.argmax(y_dists, dim=1)
    y_pred.detach()
    return y_pred.numpy()


def main(args):
    model_folder_path = f"models/{args.model_folder}"

    test_set_path = args.test_set_path
    model_path = get_model_from_folder(model_folder_path, use_latest_checkpoint=args.use_latest_checkpoint)

    if model_path is None:
        raise FileNotFoundError("No model found in folder:", model_folder_path)
    else:
        model_path = f"{model_folder_path}/{model_path}"

    encoder_folder = model_folder_path
    print("Supplied data path:", test_set_path)
    print("Model path:", model_path)

    vectorizer, label_encoder = unpickle_objects(
        f"{encoder_folder}/{VECTORIZER_FILE}",
        f"{encoder_folder}/{LABEL_ENCODER_FILE}"
    )

    checkpoint = torch.load(model_path)
    input_dim = len(vectorizer.get_feature_names())
    output_dim = len(label_encoder.classes_)

    model = DenseNeuralClassifier(input_dim, output_dim, checkpoint.get("hidden_layers", 2))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    X_test, y_test = load_signal_data(
        test_set_path,
        feature_encoder=vectorizer,
        label_encoder=label_encoder,
        fit_encoders=False
    )

    X_test_tensor = csr_to_float_tensor(X_test)
    y_pred = predict_classes(X_test_tensor, model)
    print(y_test)
    print(y_pred)
    if args.as_markdown:
        report_dict = metrics.classification_report(
            y_test, y_pred,
            target_names=label_encoder.classes_,
            output_dict=True)
        report_df = pd.DataFrame(report_dict)
        report = report_df.T.to_markdown()
    else:
        report = metrics.classification_report(
            y_test, y_pred,
            target_names=label_encoder.classes_
        )
    print(report)
    print("Average accuracy:", metrics.accuracy_score(y_test, y_pred))


if __name__ == "__main__":
    args = parse_args()
    main(args)
