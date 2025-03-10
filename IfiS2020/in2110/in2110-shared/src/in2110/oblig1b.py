from collections import Counter

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from .oblig1 import *

SENT = ['<s>', '-', 'produksjonsfall', 'i', 'august', 'har', 'samanheng', 'med',
        'revisjonsstansar', 'for', 'vedlikehald', 'på', 'fleire', 'felt', ',',
        'seier', 'vaage', 'melberg', '.', '</s>']

def visualize_word_vectors(vw, words):
    if words is None:
        words = vw.matrix.keys()

    vectors = [Counter(vec) for vec in vw.transform(words)]
    vocab = set(key for vec in vectors for key in vec.keys())

    arr = np.zeros((len(vectors), len(vocab)))

    for i,vec in enumerate(vectors):
        for j,w in enumerate(vocab):
            arr[i,j] = vec[w]

    X = PCA(2).fit_transform(arr)

    plt.figure()

    plt.scatter(X[:, 0], X[:, 1])
    for label, x, y in zip(words, X[:, 0], X[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')

    if GUI:
        plt.show()
    else:
        save_plot("word-vectors")

def assertEqual(a, b):
    assert a == b, "{} != {}".format(a, b)
    print("OK")

def test_context_window(fn):
    pos = 4
    size = 2
    correct = ['produksjonsfall', 'i', 'har', 'samanheng']

    assertEqual(fn(SENT, pos, size),
                correct)

def test_word_vectorizer(WordVectorizer):
    vec = WordVectorizer(10, 2)

