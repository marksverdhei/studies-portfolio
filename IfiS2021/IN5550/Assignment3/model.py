from transformers import BertModel
from torch import nn
import config


class NERmodel(nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self._bert = BertModel.from_pretrained(config.NORBERT_HUGGINGFACE_PATH)

        # To allow or not to allow for fine-tuning.
        # for param in self._bert.parameters():
        #     param.requires_grad = False

        self._head = nn.Linear(config.OUT_DIM, num_labels)

    def forward(self, batch, mask):
        b = self._bert(batch)
        # Handy trick from lecture
        pooler = b.last_hidden_state[:, mask].diagonal().permute(2, 0, 1)
        return self._head(pooler)
