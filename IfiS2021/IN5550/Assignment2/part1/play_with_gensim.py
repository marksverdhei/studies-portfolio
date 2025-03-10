#!/bin/env python3
# coding: utf-8
import sys
import gensim
import logging
import zipfile
import json
import random
from typing import List
import argparse

DEFAULT_OUT_PATH = "./output.txt"

CONTENT_WORD_CLASSES = ["NOUN", "ADJ", "VERB", "ADV"]


def get_words_from_file(path: str) -> List[str]:
    word_list = []
    with open(path, "r") as f:
        list_of_words = f.read().splitlines()

    for word in list_of_words:
        word_class = word.split("_")[1]
        if (word_class in CONTENT_WORD_CLASSES):
            word_list.append(word)

    return word_list


def write_to_file(path: str, result) -> None:
    print(f"Saving results to file at path  {path}")
    with open(path, 'w') as f:
        for word, similarity in result.items():
            f.write(word + ": " + str(similarity) + "\n")


def load_embedding(modelfile):
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("model_path", type=str,
                        help="The file path to the gensim model to be used.")

    parser.add_argument("input_path", type=str,
                        help="The path to the text file containing the words to be analysed.")

    parser.add_argument("output_path", type=str,
                        help="The path to save the results to")

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    logger.info("Loading the embedding model...")
    model = load_embedding(args.model_path)
    logger.info("Finished loading the embedding model...")

    logger.info(f"Model vocabulary size: {len(model.vocab)}")

    logger.info(
        f"Random example of a word in the model: {random.choice(model.index2word)}")

    words = get_words_from_file(args.input_path)

    result = {}

    for word in words:
        if word in model:
            print("=====")
            print("Associate\tCosine")
            for i in model.most_similar(positive=[word], topn=5):
                print(f"{i[0]}\t{i[1]:.3f}")
                result[i[0]] = i[1]
            print("=====")
        else:
            print(f"{word} is not present in the model")

    write_to_file(args.output_path, result)


if __name__ == "__main__":
    args = parse_args()
    main(args)
