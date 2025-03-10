
import os
from collections import defaultdict

import numpy as np
import pandas as pd
import PIL.Image

import torch
from torch.utils.data import Dataset


class VocDataset(Dataset):
    """
    Object for 'Visual Object Classes' dataset
    """

    def __init__(self, root_dir: str, set_type: str, transform=None):
        self.set_type = set_type
        self.path_handler = path_handler = PathHandler(root_dir)
        self.classes = path_handler.list_image_sets()

        self.encoder = {c:i for i, c in enumerate(self.classes)}
        self.labeled_paths = self._get_labeled_paths()

        self.transform = transform

    def __len__(self):
        return len(self.labeled_paths)

    def __getitem__(self, idx):
        root_dir = self.path_handler.root_dir
        img_name, label_vec = self.labeled_paths[idx]

        img_path = os.path.join(root_dir, "JPEGImages", img_name + ".jpg")
        image = PIL.Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, label_vec

    def _get_labeled_paths(self):
        n_classes = len(self.classes)
        img_dict = defaultdict(lambda: torch.zeros(n_classes))

        for category in self.classes:
            category_idx = self.encoder[category]
            img_paths = self.path_handler.imgs_from_category_as_list(category, self.set_type)
            for img_path in img_paths:
                img_dict[img_path][category_idx] = 1.

        return list(img_dict.items())


class PathHandler:
    """
    Handle Pascal VOC dataset
    """
    IMAGE_SETS = [
        'aeroplane', 'bicycle', 'bird', 'boat',
        'bottle', 'bus', 'car', 'cat', 'chair',
        'cow', 'diningtable', 'dog', 'horse',
        'motorbike', 'person', 'pottedplant',
        'sheep', 'sofa', 'train', 'tvmonitor'
    ]

    def __init__(self, root_dir):
        """
        Summary:
            Init the class with root dir
        Args:
            root_dir (string): path to your voc dataset
        """
        self.root_dir = root_dir
        self.img_dir = os.path.join(root_dir, 'JPEGImages/')
        self.ann_dir = os.path.join(root_dir, 'Annotations')
        self.set_dir = os.path.join(root_dir, 'ImageSets', 'Main')
        self.cache_dir = os.path.join(root_dir, 'csvs')
        # if not os.path.exists(self.cache_dir):
        #     os.makedirs(self.cache_dir)

    def list_image_sets(self):
        """
        Summary:
            List all the image sets from Pascal VOC. Don't bother computing
            this on the fly, just remember it. It's faster.
        """
        return self.IMAGE_SETS

    def _imgs_from_category(self, category, dataset):
        """
        Summary:
        Args:
            category (string): Category name as a string (from list_image_sets())
            dataset (string): "train", "val", "train_val", or "test" (if available)
        Returns:
            pandas dataframe: pandas DataFrame of all filenames from that category
        """
        filename = os.path.join(self.set_dir, category + "_" + dataset + ".txt")

        df = pd.read_csv(
            filename,
            delim_whitespace=True,
            header=None,
            names=['filename', 'true']
        )

        return df

    def imgs_from_category_as_list(self, category, dataset):
        """
        Summary:
            Get a list of filenames for images in a particular category
            as a list rather than a pandas dataframe.
        Args:
            category (string): Category name as a string (from list_image_sets())
            dataset (string): "train", "val", "train_val", or "test" (if available)
        Returns:
            list of srings: all filenames from that category
        """
        df = self._imgs_from_category(category, dataset)
        df = df[df['true'] == 1]
        return df['filename'].values
