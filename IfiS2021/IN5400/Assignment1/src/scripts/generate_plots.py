import torch
import pandas as pd
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
from functools import partial
import numpy as np
from tqdm import tqdm
from data_utils import VocDataset


def main():
    dataset = VocDataset("data/cluster_data/VOCdevkit/VOC2012/", "val")
    df = pd.read_csv("image_preds.csv", index_col=0)

    data_labels = dict(dataset.labeled_paths)

    mpl.style.use("ggplot")
    plt.title("Tail accuracy for threshold t on each class")
    plt.xlabel("t")
    plt.ylabel("tailacc(t)")

    ts = [0.05*i for i in range(1, 20)]
    all_tailaccs = []
    for label in tqdm(df.columns):
        probs = df[label]
        label_idx = dataset.encoder[label]
        targets = np.array([data_labels[img_path][label_idx].item() for img_path in df.index])
        class_tailacc = partial(tailacc, probs, targets)

        tailaccs = [class_tailacc(t) for t in ts]
        all_tailaccs.append(tailaccs)
        plt.plot(ts, tailaccs, label=label)
        # print("Tailacc for class", label, "t = 0.5", class_tailacc(0.5))

    plt.legend()
    plt.show()
    plt.legend()
    plt.title("Average tailacc for each class")
    plt.plot(ts, np.mean(all_tailaccs, axis=0), label="mean tailacc")
    plt.xlabel("t")
    plt.ylabel("tailacc(t)")
    plt.show()

def tailacc(probs, targets, t):
    denom = (probs > t).sum()
    sigma = sum(((pi > t) and ti) for pi, ti in zip(probs, targets))
    return sigma / denom


if __name__ == '__main__':
    main()
