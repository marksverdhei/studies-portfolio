import os
import time
import json
import numpy as np

import torch
from torch import nn
from torch import optim
from torch import Tensor
from torch.optim import lr_scheduler

import torchvision
from torchvision import datasets, models, transforms, utils
from torch.utils.data import Dataset, DataLoader

from sklearn import metrics
from data_utils import VocDataset

import argparse
import logging
from tqdm import tqdm

PREDICTION_THRESHOLD = 0.5

NUMBER_OF_CLASSES = 20
DEFAULTCONFIG = {
    'root_dir': "data/cluster_data/VOCdevkit/VOC2012/",
    'use_gpu': False,
    'lr': 0.005,
    'batchsize_train': 16,
    'batchsize_val': 64,
    'epochs': 35,
    'scheduler': {
        'step_size': 10,
        'factor': 0.3
    },
    'model_folder': os.path.join("bin", "checkpoints"),
    'load_model': False,
    'seed': 42,
}


data_transforms = {
    'train': transforms.Compose([
        transforms.Resize(256),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}


def make_model(cuda=False, logits=False, freeze=True):
    model = models.resnet18(pretrained=True)
    last_hidden_dim = model.fc.in_features

    if freeze:
        for param in model.parameters():
            param.requires_grad = False

    # overwrite last linear layer

    if logits:
        model.fc = nn.Linear(last_hidden_dim, NUMBER_OF_CLASSES)
    else:
        model.fc = nn.Sequential(
            nn.Linear(last_hidden_dim, NUMBER_OF_CLASSES),
            nn.Sigmoid()
        )

    if cuda:
        model = model.to("cuda")

    return model


def train_epoch(model, trainloader, criterion, optimizer, cuda=False):
    losses = []
    model.train()

    for batch_idx, data in tqdm(enumerate(trainloader), total=len(trainloader)):
        inputs, labels = data
        if cuda:
            inputs = inputs.to("cuda")
            labels = labels.to("cuda")

        optimizer.zero_grad()
        outputs = model(inputs)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    return np.mean(losses)


def predict_test(model, testloader, cuda=False):
    return probs_to_pred(predict_proba_test(model, testloader, cuda))


def probs_to_pred(probs, threshold=PREDICTION_THRESHOLD):
    return (probs > threshold).double()


def predict_proba_test(model, testloader, cuda=False):
    model.eval()
    with torch.no_grad():
        predictions = [model(X.to("cuda") if cuda else X) for X, _ in tqdm(testloader)]
    return torch.vstack(predictions)


def get_targets(testloader):
    return torch.vstack([y for _, y in testloader])


def train_eval_model(trainloader,
                     testloader,
                     model,
                     criterion,
                     optimizer,
                     scheduler,
                     config):
    num_epochs = config.get("epochs", 1)
    use_gpu = config.get("use_gpu", False)
    n_classes = NUMBER_OF_CLASSES

    best_measure = 0
    best_epoch = 0

    train_losses = []
    val_losses = []
    map_scores = []
    current_best_map = 0

    y_test = get_targets(testloader)

    if use_gpu:
        y_test = y_test.to('cuda')

    for epoch in range(num_epochs):
        logging.info('Epoch {}/{}'.format(epoch, num_epochs - 1))
        logging.info('-' * 10)

        train_loss = train_epoch(model, trainloader, criterion, optimizer, cuda=use_gpu)
        train_losses.append(train_loss)

        probabilities = predict_proba_test(model, testloader, cuda=use_gpu)
        val_loss = criterion(probabilities, y_test)
        val_losses.append(val_loss.item())

        if config.get("logits"):
            probabilities = torch.sigmoid(probabilities)

        map_score = metrics.average_precision_score(
            y_test.to("cpu") if use_gpu else y_test,
            probabilities.to("cpu") if use_gpu else probabilities
        )

        predictions = probs_to_pred(probabilities)

        logging.info(f'train loss: {train_loss}')
        logging.info(f'val loss: {val_loss}')
        logging.info(f'MAP score: {map_score}')

        map_scores.append(map_score)

        if scheduler is not None:
            scheduler.step()

        if map_score > current_best_map:
            best_weights = model.state_dict()
            optimizer_state = optimizer.state_dict()
            # track current best performance measure and epoch
            # save your scores
            model_path = os.path.join(config["model_folder"], f"model_epoch{epoch}.pt")

            torch.save({
                "model_state": best_weights,
                "optimizer_state": optimizer_state,
                "epoch": epoch,
                "train_loss": train_losses,
                "val_loss": val_losses,
                "map_score": map_scores,
                "config": config,
            }, model_path)

            current_best_map = map_score


def main(config=DEFAULTCONFIG):
    if not os.path.exists(config["model_folder"]):
        os.mkdir(config["model_folder"])

    np.random.seed(config["seed"])
    torch.manual_seed(config["seed"])

    splits = ("train", "val")

    logits = config.get("logits", False)

    image_datasets = {
        name: VocDataset(config['root_dir'], name, data_transforms[name])
        for name in splits
    }

    dataloaders = {
        "train": DataLoader(image_datasets['train'], batch_size=config['batchsize_train'], shuffle=True),
        "val": DataLoader(image_datasets['val'], batch_size=config['batchsize_val'], shuffle=False)
    }

    logging.info(f"Train samples: {len(image_datasets['train'])}")
    logging.info(f"Train batches: {len(dataloaders['train'])}")
    logging.info(f"Val samples: {len(image_datasets['val'])}")
    logging.info(f"Val batches: {len(dataloaders['val'])}")

    use_gpu = config.get('use_gpu', False)
    freeze = config.get('freeze', True)

    model = make_model(cuda=use_gpu, logits=logits, freeze=freeze)

    if logits:
        criterion = torch.nn.BCEWithLogitsLoss()
    else:
        criterion = torch.nn.BCELoss()


    # Observe that all parameters are being optimized
    if config.get("adam", False):
        optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'])
    else:
        optimizer = torch.optim.SGD(model.parameters(), lr=config['lr'])

    # Decay LR by a factor of 0.3 every X epochs
    scheduler_config = config.get("scheduler")
    if scheduler_config:
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer,
            scheduler_config['step_size'],
            gamma=scheduler_config['factor']
        )
    else:
        scheduler = None

    train_eval_model(
        dataloaders['train'],
        dataloaders['val'],
        model,
        criterion,
        optimizer,
        scheduler,
        config=config
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str,
                        help="JSON file that contains all the configurations for the model")

    args = parser.parse_args()

    config = DEFAULTCONFIG
    if args.config:
        with open(args.config, "r") as f:
            config.update(json.load(f))

    logging.basicConfig(level=logging.INFO)

    main(config)
