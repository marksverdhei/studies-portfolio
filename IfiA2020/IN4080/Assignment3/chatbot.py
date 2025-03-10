import os, random, gzip, json, re
import tensorflow as tf
import tensorflow.keras as keras
import encoder_client
import numpy as np
import itertools

# For serialization
import pickle

DIALOGUE_FILE = "data/en-comedy.txt.gz"
FIRST_NAMES = "data/first_names.json"
MODEL_URI = "https://nr.no/~plison/data/model.tar.gz"


class Chatbot:
    """A dual encoder model for a Retrieval chatbot"""

    def __init__(self, dialogue_data=DIALOGUE_FILE, embedding_path=None, random_state=None):
        """Initialises a chatbot based on a Dual Encoder architecture, with
        utterances encoded using the pre-trained ConveRT model
        (https://arxiv.org/abs/1911.03688)."""

        if random_state is not None:
            np.random.seed(random_state)
            tf.random.set_seed(random_state)

        # Loads the ConveRT utterance encoder
        self.client = encoder_client.EncoderClient(MODEL_URI)
        if embedding_path and os.path.exists(embedding_path):
            with open(embedding_path, "rb") as f:
                self.pairs, self.responses, self.response_embeddings = pickle.load(f)
        else:
            # Extracts the (context, response) pairs
            self.pairs = self._extract_pairs(dialogue_data)

            # Compute the embeddings for the responses (takes some time to compute!)
            self.responses = [response for _, response in self.pairs]
            self.response_embeddings = self.client.encode_responses(self.responses)

            if embedding_path:
                with open(embedding_path    , "wb+") as f:
                    pickle.dump([self.pairs, self.responses, self.response_embeddings], f)


    def _extract_pairs(self, dialogue_data, max_nb_pairs=100000):
        """Given a file containing dialogue data, extracts a list of relevant
        (context,response) pairs, where both the context and response are
        strings. The 'context' is here simply the first utterance (such as a question),
        and the 'response' the following utterance (such as an answer).

        The (context, response) pairs should satisfy the following critera:
        - The two strings should be consecutive, and part of the same movie/TV series
        - Pairs in which one string contains parentheses, brackets, colons, semi-colons
          or double quotes should be discarded.
        - Pairs in which one string is entirely in uppercase should be discarded
        - Pairs in which one string contains more than 10 words should be discarded
        - Pairs in which one string contains a first name should be discarded
          (see the json file FIRST_NAMES to detect those).

        You are of course free to add additional critera to increase the quality of your
        (context,response) pairs. You should stop the extract once you have reached
        max_nb_pairs.

        """
        a = list(self._pair_gen(dialogue_data, max_nb_pairs))
        return a


    def _pair_gen(self, dialogue_data, max_nb_pairs, separator=b"###"):
        """Auxiliary generator function for _extract_pairs
        """

        nb_pairs = 0
        with gzip.open(dialogue_data) as reader:
            if next(reader, None) is None: return
            with open("data/first_names.json") as name_file:
                names = [bytes(i, encoding="UTF8") for i in json.load(name_file)]
            iterator, empty = next(reader, None), None
            while iterator is not empty:
                prev = iterator
                for line in itertools.takewhile(lambda x: not x.startswith(separator), reader):
                    valid_punctuation = all(c not in line for c in b"()[]:;\"")
                    valid_case = not line.isupper()
                    valid_length = len(line.split()) <= 10
                    valid_name = all(name not in line for name in names)

                    if valid_punctuation and valid_case and valid_length and valid_name:
                        if prev is not None:
                            yield prev, line
                            nb_pairs += 1
                            if nb_pairs >= max_nb_pairs: return
                        prev = line
                    else:
                        prev = None

                iterator = next(reader, None)


    def get_response(self, user_utterance):
        """Extracts the context embedding for the user utterance, and then computes
        the dot product of this embeddings with all the response embeddings (already
        computed in self.response_embeddings). The response with the highest dot
        product is then selected.

        To get the context embedding for the user utterance, simply use the method
        client.encode_contexts(...).

        The method returns a string with the response of the chatbot."""
        context_embedding = self.client.encode_contexts([user_utterance])
        argmax = np.argmax(self.response_embeddings @ context_embedding.T)
        return self.responses[argmax].decode("UTF8")


    def fine_tune(self, epochs=10):
        """Fine-tunes the dual encoder model by computing a transformation (linear
        transformation + non-linear ReLU activation) of the response embeddings,
        optimised on the (context, response) pairs extracted for the dataset.
        The method updates the response embeddings with the transformed values"""

        # Extract the training data (with both positive and negative examples)
        context_embeddings2, response_embeddings2, outputs = self._get_training_data()

        # Creates the two input layers (for the two embeddings)
        input1 = tf.keras.layers.Input((context_embeddings2.shape[1],))
        input2 = tf.keras.layers.Input((response_embeddings2.shape[1],))

        # Computes the transformation of the response embeddings
        dense2 = tf.keras.layers.Dense(response_embeddings2.shape[1], activation="relu")

        # Computes the dot product, and pass through a sigmoid to get a probability
        dotproduct = tf.keras.layers.Dot(axes=1)
        sigmoid = tf.keras.layers.Activation(tf.keras.activations.sigmoid)

        # Connects together all layers
        output_prob = sigmoid(dotproduct([input1, dense2(input2)]))

        # Creates a new model, specifying the inputs and output
        model = tf.keras.Model([input1, input2], output_prob)
        model.summary()

        # Compile the model the "Adam" optimiser and a cross-entropy loss
        model.compile(loss="binary_crossentropy", optimizer="adam")

        # Train the model on 10 epochs
        model.fit([context_embeddings2, response_embeddings2], outputs,
                  batch_size=32,epochs=epochs)

        # Once the model is trained, we simple transform the response embeddings using
        # the transformation we have learned
        embeddings_tensor = dense2(self.response_embeddings)
        self.response_embeddings = tf.keras.backend.eval(embeddings_tensor)


    def _get_training_data(self, context_embedding_path=None):
        """Constructs a dataset to fine-tune the dual encoder. The dataset should
        contain both positive examples (that is, pairs of context and response embeddings
        that do correspond to actual response pairs) and negative examples (pairs of context
        and response embeddings that are selected at random and are not related).

        More precisely, the method should return 3 outputs:
        - one matrix of shape (2*len(self.pairs), 512) with context embeddings from the pairs
        - one matrix of shape (2*len(self.pairs), 512) with response embeddings from the pairs
        - one array of shape 2*len(self.pairs) with binary values

        Half of the training examples should be positive (actual pair of embeddings) and half
        should be negative (pair of embeddings selected at random), which is why the total length
        of the training data is twice the number of (context, response) pairs. For positive examples,
        the corresponding value in the output array should be 1, and 0 for negative examples.

        The response embeddings have already been computed (in self.response_embeddings) so you
        don't need to compute them again. But you need to compute the context embeddings for your
        pairs using the method client.encode_contexts(contexts).

        Note that the positive and negative examples should be shuffled (to avoid confusing the
        machine learning model by first starting with only positive examples, then having only
        negative examples).
        """
        # N will be the size of ur pairs
        k = len(self.pairs)
        N = 2*k

        if not hasattr(self, "context_embeddings"):
            if context_embedding_path and os.path.exists(context_embedding_path):
                with open(context_embedding_path, "rb") as f:
                    self.contexts, self.context_embeddings = pickle.load(f)
            else:
                self.contexts = [c for c, _ in self.pairs]
                self.context_embeddings = self.client.encode_responses(self.contexts)
                if context_embedding_path:
                    with open(context_embedding_path, "wb+") as f:
                        pickle.dump((self.contexts, self.context_embeddings), f)
                        print("Sucessfully wrote to", context_embedding_path)

        negative_responses = self.response_embeddings.copy()
        np.random.shuffle(negative_responses)

        context = np.concatenate((self.context_embeddings, self.context_embeddings))
        response = np.concatenate((self.response_embeddings, negative_responses))
        target = np.concatenate((np.ones(k), np.zeros(k)))

        perm = np.random.permutation(N)

        return context[perm], response[perm], target[perm]


if __name__ == "__main__":
    cb = Chatbot(embedding_path=False)
    print(cb.pairs)
    # context = input(">")
    # while context.lower() not in "quit":
    #     print("\nBot:", cb.get_response(context), end="\n")
    #     context = input(">")
