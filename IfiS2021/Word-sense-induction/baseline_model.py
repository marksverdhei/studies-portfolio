import gensim
import zipfile
import json
import random
from collections import Counter


def egvi(target_word, embedder, N=50, K=50, clustering_iterations=10):
    print(f"Executing egvi algorithm for word {target_word} with N={N} and K={K}.")
    word_vector = embedder[target_word]
    vocab = embedder.index2word

    # Constructing N
    n_most_similar_words = [w for w, sim in embedder.most_similar(positive=[target_word], topn=N)]
    
    # Constructing ∆
    deltas = [word_vector - embedder[w] for w in n_most_similar_words]
    
    # Constructing ¬N and V
    n_complement = []
    ego_graph = {}

    for delta, word in zip(deltas, n_most_similar_words):
        distances = [(i, dist) for i, dist in enumerate(embedder.distances(delta, other_words=vocab))]
        distances = sorted(distances, key= lambda x : x[1])

        if vocab[distances[0][0]] == target_word:
            # most similar anti-pair is the target word itself, use second most similar
            anti_word = vocab[distances[1][0]]
        else:
            anti_word = vocab[distances[0][0]]
        
        #print(f"Anti-edge: ({word},{anti_word})")

        # add anti-pair to ¬N
        n_complement.append(anti_word)

        # only add word to V if both the word and its anti-pair are in N
        if anti_word in n_most_similar_words:
            ego_graph[word] = {"neighbours": set()}
            ego_graph[anti_word] = {"neighbours": set()}

    if len(ego_graph) == 0:
        print("No vertices added to graph, try with a bigger N")
        exit()

    # Constructing E (after all vertices have been added to V)
    for word, anti_word in zip(n_most_similar_words, n_complement):
        if word in ego_graph:
            k_most_similar_words = [w for w, sim in embedder.most_similar(positive=[word], topn=K)]
            for u in k_most_similar_words:
                # we dont add anti-edges to the graph
                if (u in ego_graph) and (u != anti_word):
                    print(f"Adding edge to the graph: ({word},{u})")
                    ego_graph[word]["neighbours"].add(u)
                    ego_graph[u]["neighbours"].add(word)
    

    # Chinese Whispers clustering
    for i, w in enumerate(ego_graph):
        ego_graph[w]["class"] = i
    
    random.seed(42)
    vertices = list(ego_graph.keys())

    for i in range(clustering_iterations):
        random.shuffle(vertices)
        for w in vertices:
            neighbouring_clusters = Counter([ego_graph[neighbour]["class"] for neighbour in ego_graph[w]["neighbours"]])
            ego_graph[w]["class"] = neighbouring_clusters.most_common(1)[0][0]

    clusters = {node["class"]:[] for _, node in ego_graph.items()}
    for word, node in ego_graph.items():
        clusters[node["class"]].append(word)

    # Defining keywords/sense names
    anti_edge_counter = Counter(n_most_similar_words+n_complement)
    named_clusters = {}
    for key in clusters:
        class_counts = [(word, anti_edge_counter[word]) for word in clusters[key]]
        best_word = sorted(class_counts, key= lambda x : x[1])[0][0]
        named_clusters[best_word] = clusters[key]

    return named_clusters

def load_embedding(modelfile):
    """ Loads gensim embeddings from NLPL vector repository.
        Args:
            modelfile (string): Path to a gensim model

        Returns:
            (gensim.models.keyedvectors.Word2VecKeyedVectors): gensim embedder
    """
    # ZIP archive from the NLPL vector repository:
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
                "model.bin"  # or model.txt, if you want to look at the model
            )
            emb_model = gensim.models.KeyedVectors.load_word2vec_format(
                stream, binary=True, unicode_errors="replace"
            )
        emb_model.init_sims(replace=True)
        return emb_model

    else:
        print("Wrong file format")
        exit()



if __name__ == "__main__":
    embedder = load_embedding("/cluster/shared/nlpl/data/vectors/latest/82.zip")

    #egvi("add", embedder)
    #egvi("trace", embedder)
    egvi("paper", embedder, 50, 50)