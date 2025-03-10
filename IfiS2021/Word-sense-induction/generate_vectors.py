from transformers import PreTrainedTokenizerFast
from transformers import BertTokenizerFast, BertModel
# from transformers import DebertaTokenizer, DebertaModel
from transformers import RobertaTokenizerFast, RobertaModel

import pandas as pd
from tqdm import tqdm
import torch
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from functools import partial

tqdm.pandas()

dataset_path = "data/SemEval-2013-Task-13-test-data/semeval_with_labels.csv"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df = pd.read_csv(dataset_path)

model_type = "bert"

if model_type == "bert":
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased").to(device)
elif model_type == "roberta":
    tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")
    model = RobertaModel.from_pretrained("roberta-base").to(device)
else:
    raise TypeError("invalid model type")

# tokenizer = DebertaTokenizer.from_pretrained('microsoft/deberta-base')
# model = DebertaModel.from_pretrained('microsoft/deberta-base').to(device)

def find_idx_for_slow_tokenizer(x):
    text_masked = x[:]
    tokens = tokenizer(
        x["text"],
        return_tensors="pt",
    )

    raise NotImplementedError()

def find_idx_for_fast_tokenizer(x):
    tokens = tokenizer(
        x["text"],
        return_tensors="pt",
        return_offsets_mapping=True
    )

    span = s, e = x["tokenStart"], x["tokenEnd"]
    token_ids = tokens["input_ids"]

    token_ids = token_ids[1:-1]
    token_ranges = tokens["offset_mapping"].squeeze()[1:-1]

    token_starts, token_ends = token_ranges.T

    start_idx = torch.where(token_starts == s)[0][0]
    end_idx = torch.where(token_ends == e)[0][0]

    return tokens, (start_idx, end_idx)


def generate_embedding(x: pd.Series):
    if isinstance(tokenizer, PreTrainedTokenizerFast):
        tokens, (start_idx, end_idx) = find_idx_for_fast_tokenizer(x)
    else:
        tokens, (start_idx, end_idx) = find_idx_for_slow_tokenizer(x)

    idx_span = torch.arange(start_idx, end_idx+1)

    with torch.no_grad():
        embeddings, = model(
            tokens.input_ids.to(device),
            attention_mask=tokens.attention_mask.to(device)
        ).last_hidden_state

    target_embeddings = embeddings[idx_span]
    target_embedding = target_embeddings.mean(axis=0)

    emb_array = target_embedding.cpu().numpy()
    return x.append(pd.Series(emb_array))


def inventory_for_words():
    model.eval()

    df_with_embeddings = df.progress_apply(generate_embedding, axis=1, result_type="expand")

    return df_with_embeddings



if __name__ == '__main__':
    generated_embeddings = inventory_for_words()
    embedding_df = generated_embeddings.loc[:, 0:]
    embedding_df.insert(0, "id", generated_embeddings["id"])
    embedding_df.to_csv("bert_base_embeddings.csv", index=False)
