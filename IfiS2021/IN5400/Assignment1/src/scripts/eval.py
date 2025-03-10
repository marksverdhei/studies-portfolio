import pandas as pd

import torch
from torch.utils.data import DataLoader
from torchvision import transforms

from sklearn import metrics

from train import make_model, get_targets, predict_proba_test, probs_to_pred
from data_utils import VocDataset
import argparse

THRESHOLD = 0.5
ROOT_DIR = "data/cluster_data/VOCdevkit/VOC2012/"
DEFAULT_CHECKPOINT_PATH = "bin/checkpoints/model_epoch30.pt"
BATCH_SIZE = 64

def main(set_type,
         cuda=False,
         root_dir=ROOT_DIR,
         checkpoint_path=DEFAULT_CHECKPOINT_PATH,
         batch_size=BATCH_SIZE,
         threshold=THRESHOLD,
         **kwargs):
    print("Kwargs:", kwargs)

    device = torch.device("cuda") if cuda else torch.device("cpu")
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model = make_model(cuda)
    model.load_state_dict(checkpoint["model_state"])

    model.eval()

    test_transform = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        # We dont do autgmentation at Evaluation
        # transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load data
    dataset = VocDataset(root_dir, set_type, test_transform)
    testloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    y_test = get_targets(testloader)

    y_pred_probs = predict_proba_test(model, testloader, cuda=cuda)
    y_pred = probs_to_pred(y_pred_probs)

    print("mAP", metrics.average_precision_score(y_test, y_pred_probs))

    filenames = [i for i, _ in dataset.labeled_paths]
    df_dict = {"filenames": filenames}
    df_dict.update({
        dataset.classes[i]:preds for i, preds in enumerate(y_pred_probs.T)
    })

    pd.DataFrame(df_dict).to_csv("image_preds.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint_path", type=str)
    parser.add_argument("--root_dir", type=str, default=ROOT_DIR)
    parser.add_argument("--val", action="store_true")
    parser.add_argument("--cuda", action="store_true")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE)
    args = parser.parse_args()

    # set_type = "val" if args.val else "test"
    set_type = "val"

    main(set_type, **vars(args))
