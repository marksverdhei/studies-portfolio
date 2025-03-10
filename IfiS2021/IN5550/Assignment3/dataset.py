from torch.utils.data import Dataset
import torch


class NERdata(Dataset):
    def __init__(self, data, label_vocab=None):
        self.data = data
        self.label_vocab = label_vocab if label_vocab else list(
            set([token["misc"]["name"] for text in data for token in text]))
        self.label_vocab.extend(['@UNK'])
        self.label_indexer = {i: n for n, i in enumerate(self.label_vocab)}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx]
        text = [token["form"] for token in x]
        label = [token["misc"]["name"] for token in x]

        Y = torch.LongTensor(
            [self.label_indexer[i] if i in self.label_vocab else self.label_indexer['@UNK'] for i in label])

        return text, Y
