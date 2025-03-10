from typing import Any, Callable, Iterable, List
from functools import partial
import operator
import zipfile
import json
from transformers import BertTokenizer, BertModel
from gensim.scripts.glove2word2vec import glove2word2vec
from transformers import MobileBertTokenizer, MobileBertModel

import numpy as np
import gensim
import torch
from torch import nn

GLOVE_TAGGED_PATH = "../bin/embeddings/glove_tagged_13.zip"
W2V_UNTAGGED_PATH = "../bin/embeddings/word2vec_untagged_12.zip"
W2V_TAGGED_PATH = "../bin/embeddings/word2vec_tagged_200.zip"
W2V_TAGGED_FUNCWORDS_PATH = "../bin/embeddings/40.zip"
FASTTEXT_PATH = "../bin/embeddings/fasttext_tagged_15.zip"


class TextToBertEmbedding(torch.nn.Module):

    embed_dims = 512

    def __init__(self, fine_tune=False):
        super(TextToBertEmbedding, self).__init__()
        # cannot change (taken from the config of the BERT model)
        self.tokenizer = MobileBertTokenizer.from_pretrained(
            'google/mobilebert-uncased')
        self.bert = MobileBertModel.from_pretrained(
            'google/mobilebert-uncased')

        if not fine_tune:
            for p in self.bert.parameters():
                p.requires_grad = False

    def forward(self, batch):
        batch = list(batch)
        encoding = self.tokenizer(batch, return_tensors='pt', padding=True)
        activations = self.bert(**encoding)
        embeddings = activations.last_hidden_state
        return embeddings


class TextToEmbedding(torch.nn.Module):
    "Tokenizer takes in sentences and returns word embeddings"

    def __init__(self, tokenizer, vectors, fixed_size=None, freeze_embeddings=True, *args, **kwargs):
        """
        tokenizer:
            function that takes in raw text documents and returns an arraylike of token indices
            supported by the word embedding model and returns indices.

        vectors:
            Vectors to apply to the embedding layers
        """
        super(TextToEmbedding, self).__init__()

        self.tokenize = tokenizer

        self.embed = nn.Embedding.from_pretrained(
            torch.FloatTensor(vectors),
            freeze=freeze_embeddings
        )

        self.fixed_size = fixed_size
        self.embed_dims = vectors.shape[1]

    def forward(self, batch):
        tokens = [self.tokenize(x) for x in batch]
        batch_size = len(tokens)

        pad_size = self.fixed_size or max(map(len, tokens))

        token_matrix = torch.zeros(batch_size, pad_size, dtype=int)
        for i, doc in enumerate(tokens):
            for j, t in enumerate(doc[:pad_size]):
                token_matrix[i, j] = t

        embeddings = self.embed(token_matrix)
        return embeddings


class Lambda(torch.nn.Module):
    """
    Lambda layer that takes in an arbitrary function to pass in a
    sequential model
    """

    def __init__(self, f):
        super(Lambda, self).__init__()
        self.f = f

    def forward(self, x):
        return self.f(x)


class RNNCLassifier(nn.Module):
    def __init__(self, preprocessor, rnn_type="rnn", rnn_layers=2, hidden_size=200, bidirectional=True):
        super().__init__()

        rnn_out_dim = hidden_size
        if bidirectional:
            rnn_out_dim *= 2

        rnn_types = {
            "rnn": nn.RNN,
            "lstm": nn.LSTM,
            "gru": nn.GRU,
        }

        rnn_layer = rnn_types[rnn_type]
        self.preprocessor = preprocessor
        self.hidden_size = hidden_size
        self.rnn = rnn_layer(input_size=self.preprocessor.embed_dims, hidden_size=self.hidden_size, num_layers=rnn_layers,
                             bidirectional=bidirectional, batch_first=True)
        self.dense = nn.Linear(rnn_out_dim, hidden_size)
        self.relu = nn.ReLU()
        self.linear = nn.Linear(self.hidden_size, 1)
        self.fn = nn.Sigmoid()

    def forward(self, batch):
        embeddings = self.preprocessor(batch)
        o, h = self.rnn(embeddings)
        o = self.dense(o)
        o = self.relu(o)
        o = self.linear(o[:, -1, :])
        return self.fn(o)


def make_classifier(model_type: str, embedding_type: str, *args, **kwargs) -> Callable:
    """
    Returns a pytorch classifier with inupt shape
    equal that of the word embeddings
    """
    model_type = model_type.lower()
    embedding_type = embedding_type.lower()

    preprocessor = make_embedding_layer(embedding_type)

    if model_type in ("linear", "logreg", "dense", "feedforward"):
        inputmethod = kwargs.get("inputmethod", "fixed_size")
        fixed_size = kwargs.get("fixed_size", 52)
        def fix_size(batch):
            batch_size, sent_length, vec_dim = batch.shape
            target = torch.zeros(batch_size, fixed_size, vec_dim)
            target[:, :sent_length, :] = batch
            target = target.flatten(1)
            return target

        convert_function = {
            "fixed_size": fix_size,
            "average": partial(torch.mean, axis=1),
            "sum": partial(torch.sum, axis=1),
        }.get(inputmethod, None)

        if not convert_function:
            raise NotImplementedError(
                f"Input method {inputmethod} not implemented")

        hidden_layers = []
        embed_dims = preprocessor.embed_dims

        first_layer_input = embed_dims
        if inputmethod == "fixed_size":
            first_layer_input *= fixed_size


        if model_type in ("dense", "feedforward"):
            first_layer_output = embed_dims
            num_hidden_layers = kwargs.get("hidden_layers", 0)
            hidden_layers.append(nn.ReLU())
            for i in range(num_hidden_layers):
                hidden_layers.append(nn.Linear(embed_dims, embed_dims))
                hidden_layers.append(nn.ReLU())
            hidden_layers.append(nn.Linear(embed_dims, 1))
        else:
            first_layer_output = 1

        model = nn.Sequential(
            preprocessor,
            Lambda(convert_function),
            nn.Linear(first_layer_input, first_layer_output),
            *hidden_layers,
            nn.Sigmoid()
        )
        return model

    elif model_type in ("rnn", "lstm", "gru"):
        model = RNNCLassifier(
            preprocessor,
            model_type,
            rnn_layers=kwargs.get("hidden_layers", 2),
            bidirectional=kwargs.get("bidirectional", True),
            hidden_size=kwargs.get("hidden_layer_size", 200),
        )

        return model

    elif model_type == "cnn":
        raise NotImplementedError("CNNs not implemented")
    else:
        raise ValueError(f"{model_type} is not a valid model type\n"
                         "valid types are: dense, rnn")


def make_embedding_layer(model_type: str,
                         tokenizer: Callable = lambda x: x.split(" "),
                         *args, **kwargs) -> nn.Module:
    """
    Returns a word embedding model based on the given model type input
    """
    model_type = model_type.lower()

    if model_type == "word2vec":
        model_path = kwargs.get("model_path", W2V_TAGGED_PATH)

        if not model_path:
            raise ValueError("Supply model path on cbow")

        model = load_gensim_model(model_path)
        model.add('<unk>', weights=torch.rand(model.vector_size))
        model.add('<pad>', weights=torch.zeros(model.vector_size))

        def indexer(x): return [
            model.vocab[t].index for t in tokenizer(x) if t in model.vocab]

        return TextToEmbedding(tokenizer=indexer, vectors=model.vectors)

    elif model_type == "fasttext":
        model_path = kwargs.get("model_path", FASTTEXT_PATH)
        fasttext_model = load_fasttext_model(model_path)

        fasttext_model.add_vector(
            '<pad>', weights=torch.zeros(fasttext_model.vectors_norm))

        def indexer(x): return [
            fasttext_model.vocab[t].index for t in tokenizer(x) if t in fasttext_model.vocab]

        return TextToEmbedding(tokenizer=indexer, vectors=fasttext_model.vectors)

    elif model_type == "glove":
        model_path = kwargs.get("model_path", GLOVE_TAGGED_PATH)

        if not model_path:
            raise ValueError("Supply model path on cbow")

        model = load_gensim_model(model_path)
        model.add('<unk>', weights=torch.rand(model.vector_size))
        model.add('<pad>', weights=torch.zeros(model.vector_size))

        def indexer(x): return [
            model.vocab[t].index for t in tokenizer(x) if t in model.vocab]

        return TextToEmbedding(tokenizer=indexer, vectors=model.vectors)

    elif model_type == "bert":
        print("Selected bert embeddings")
        return TextToBertEmbedding()

    else:
        raise ValueError(f"{model_type} is not a valid model type\n"
                         "valid types are: word2vec, fasttext, bert")


def load_gensim_model(modelfile: str) -> gensim.models.keyedvectors.Word2VecKeyedVectors:
    "Yanked directly from play_with_gensim.py"
    # Detect the model format by its extension:
    # Binary word2vec format:
    if modelfile.endswith(".bin.gz") or modelfile.endswith(".bin"):
        emb_model = gensim.models.KeyedVectors.load_word2vec_format(
            modelfile, binary=True, unicode_errors="replace"
        )
    # Text word2vec format:
    elif (
        modelfile.endswith(".txt.gz")
        or modelfile.endswith(".txt")
        or modelfile.endswith(".vec.gz")
        or modelfile.endswith(".vec")
    ):
        emb_model = gensim.models.KeyedVectors.load_word2vec_format(
            modelfile, binary=False, unicode_errors="replace"
        )
    # ZIP archive from the NLPL vector repository:
    elif modelfile.endswith(".zip"):
        with zipfile.ZipFile(modelfile, "r") as archive:
            # Loading and showing the metadata of the model:
            metafile = archive.open("meta.json")
            metadata = json.loads(metafile.read())
            for key in metadata:
                print(key, metadata[key])
            print("============")
            # Loading the model itself:
            stream = archive.open(
                "model.bin"  # or model.txt, if you want to look at the model
            )
            emb_model = gensim.models.KeyedVectors.load_word2vec_format(
                stream, binary=True, unicode_errors="replace"
            )
    else:  # Native Gensim format?
        emb_model = gensim.models.KeyedVectors.load(modelfile)
        #  If you intend to train the model further:
        # emb_model = gensim.models.Word2Vec.load(embeddings_file)
    # Unit-normalizing the vectors (if they aren't already):
    emb_model.init_sims(
        replace=True
    )
    return emb_model


def load_glove_model(modelfile: str) -> gensim.models.fasttext.FastTextKeyedVectors:
    '''
        Loads fasttext embedding swith gensim.
        args:
            modelfile (str): path to the embedding file to load
        returns:
            gensim.models.fasttext.FastTextKeyedVectors
    '''
    if modelfile.endswith(".zip"):
        with zipfile.ZipFile(modelfile, "r") as archive:
            # Loading and showing the metadata of the model:
            metafile = archive.open("meta.json")
            metadata = json.loads(metafile.read())
            for key in metadata:
                print(key, metadata[key])
            print("============")
            # Loading the model itself:
            stream = archive.open(
                "model.txt"
            )

            word2vec_output_file = 'glove_word2vec.txt'

            glove2word2vec(stream, word2vec_output_file)

            emb_model = gensim.models.KeyedVectors.load_word2vec_format(
                word2vec_output_file, binary=False)

    emb_model.init_sims(
        replace=True
    )
    return emb_model


def load_fasttext_model(modelfile: str):
    '''
        Loads fasttext embedding swith gensim.
        args:
            modelfile (str): path to the embedding file to load
        returns:
    '''
    if modelfile.endswith(".zip"):
        with zipfile.ZipFile(modelfile, "r") as archive:
            # Loading and showing the metadata of the model:
            metafile = archive.open("meta.json")
            metadata = json.loads(metafile.read())
            for key in metadata:
                print(key, metadata[key])
            print("============")
            # Loading the model itself:
            stream = archive.open(
                "parameters.bin"
            )
            emb_model = gensim.models.fasttext.load_facebook_vectors(
                stream, encoding="utf-8"
            )

    emb_model.init_sims(
        replace=True
    )
    return emb_model
