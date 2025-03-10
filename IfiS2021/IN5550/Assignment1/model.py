import torch
from torch import nn


def DenseNeuralClassifier(n_features, n_classes, hidden_layers=2):
    """
    Returns a sequential model with 2 hidden layers or
    hidden layers equal to supplied argument
    """
    
    assert hidden_layers > 0, "Need at least 1 hidden layer"
    if hidden_layers == 1:
        model = nn.Sequential(
            nn.Linear(n_features, 200),
            nn.ReLU(),
            nn.Linear(200, n_classes),
            nn.Softmax(1)
        )
    else:
        extra_layers = []
        for i in range(hidden_layers-2):
            extra_layers.append(nn.Linear(200, 200))
            extra_layers.append(nn.ReLU())

        model = nn.Sequential(
            nn.Linear(n_features, 200),
            nn.ReLU(),
            *extra_layers,
            nn.Linear(200, 50),
            nn.ReLU(),
            nn.Linear(50, n_classes),
            nn.Softmax(1)
        )

    return model
