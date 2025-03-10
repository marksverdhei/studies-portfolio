import argparse
import numpy as np
import pandas as pd
from collections import Counter
from sklearn import preprocessing, metrics, model_selection, linear_model
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from typing import Iterable


DEFAULT_DATA_PATH = "mushroom_dataset.csv"
DEFAULT_MODEL_PATH = "./model"
DEFAULT_LABEL_FIELD = "mushroom"
DEFAULT_SEED = 420


class Net(nn.Module):
    def __init__(self, input_size=117):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, 200)
        self.fc2 = nn.Linear(200, 50)
        self.fc3 = nn.Linear(50, 20)
        self.fc4 = nn.Linear(20, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.float()
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))
        return x


def get_train_test_tensors(X: np.ndarray, y: np.ndarray, test_size: float) -> Iterable[torch.Tensor]:
    return map(torch.tensor, model_selection.train_test_split(X, y, test_size=test_size))


def load_and_preprocess_data(path: str, label_field: str, test_size=0.3) -> Iterable[torch.Tensor]:
    '''
        Loads data at provided path and executes some preprocessing.
        args:
            path (str): path to file
            label_field (str): target column name
        returns:
            X_train, X_test, y_train, y_test
    '''
    dataset = pd.read_csv(path)
    features, targets = dataset.drop(label_field, axis=1), dataset[label_field].to_numpy()
    features = features.to_numpy()[:, :3]
    feat_encoder = preprocessing.OneHotEncoder()
    X = feat_encoder.fit_transform(features)
    target_encoder = preprocessing.LabelEncoder()
    y = target_encoder.fit_transform(targets)
    features = X.toarray()
    poisonous = y # 1 if poisonous, 0 if edible
    return get_train_test_tensors(features, poisonous, test_size)


def get_model1():
    "Showcase of how to make the same model in a simpler way. Unused for now"
    model = torch.nn.Sequential(
        torch.nn.Linear(117, 200),
        torch.nn.ReLU(),
        torch.nn.Linear(200, 50),
        torch.nn.ReLU(),
        torch.nn.Linear(50, 20),
        torch.nn.ReLU(),
        torch.nn.Linear(20, 1),
        torch.Sigmoid(),
    )
    return model


def train_model(X_train, y_train, epochs=2) -> nn.Module:

    net = Net(input_size=X_train.shape[-1])

    criterion = nn.BCELoss()
    optimizer = optim.Adam(net.parameters(), lr=1e-4)


    tensor_dataset = TensorDataset(X_train, y_train)
    trainloader = DataLoader(tensor_dataset)

    running_loss = 0.0
    for epoch in range(epochs):
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            labels = labels.unsqueeze(1).float()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 2000 == 1999:
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    return net


def evaluate_classifier(X_test, y_test, net):
    y_prime = net(X_test)
    y_np = y_prime.detach().numpy()
    y_pred = (y_np.T[0] > 0.5).astype(int)
    print(y_pred)
    print(metrics.classification_report(y_test, y_pred))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="Seed for reproducibility")
    parser.add_argument("--model_path", type=str, default=DEFAULT_MODEL_PATH,
                        help="The path where the model is saved")
    parser.add_argument("--data_path", type=str, default=DEFAULT_DATA_PATH,
                        help="The path where the dataset csv lies")
    parser.add_argument("--label_field", type=str, default=DEFAULT_LABEL_FIELD,
                        help="The atrribute in the dataset we want to predict")
    parser.add_argument("--epochs", type=int, default=2,
                        help="Number of epochs to train the model")

    parser.add_argument("-t", "--test", action="store_true",
                        help="If true: load the model from the given path and test it"
                        "If false, train a new model and write it to model_path")

    parser.add_argument("--test_size", type=int, default=0.25)


    return parser.parse_args()


def set_random_seeds(seed) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


def main(args: argparse.Namespace) -> None:
    X_train, X_test, y_train, y_test = load_and_preprocess_data(args.data_path, args.label_field, test_size=args.test_size)


    if args.test:
        net = torch.load(args.model_path)
        net.eval()
        print(f"Loaded model from {args.model_path}")
    else:
        net = train_model(X_train, y_train, epochs=args.epochs)
        torch.save(net, args.model_path)
        print(f"Saved model to {args.model_path}")
        net.eval()

    evaluate_classifier(X_test, y_test, net)

    baseline = linear_model.LogisticRegression()
    baseline.fit(X_train.numpy(), y_train.numpy())
    baseline_pred = baseline.predict(X_test)

    print("LogisticRegresison:")
    print(metrics.classification_report(y_test, baseline_pred))

if __name__ == "__main__":
    args = parse_args()
    print("seed", args.seed)
    set_random_seeds(args.seed)
    main(args)
