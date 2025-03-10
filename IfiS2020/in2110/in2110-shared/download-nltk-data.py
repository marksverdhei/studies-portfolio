import nltk
import nltk.data

resources = {"punkt": "tokenizers/punkt",
             "movie_reviews": "corpora/movie_reviews"}

for name, path in resources.items():
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(name)
