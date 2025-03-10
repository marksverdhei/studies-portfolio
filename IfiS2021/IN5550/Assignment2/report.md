---
geometry: margin=2cm
output: pdf_document
---

# Word Embeddings and Recurrent Neural Networks

### IN5550 - Assignment 2

Markus S. Heiervang, Daniel Clemet, Sondre Wold

To reproduce the experiments outlined in this report, please see the code at [github.uio.no](github.uio.no/markuhei/IN5550), and follow the instructions given by the `README.md` file.  
It is a private repository but if you are an IN5550 instructor, you should have been granted access.

Libraries used:  
`numpy, pandas, sklearn, pytorch, tensorflow`

---

## Working with pre-trained models locally

### How to run

To reproduce the results for this subassignment, run the file `play_with_gensim.py`, which takes the following positional arguments: [1]`model_path`, [2]`input_path`, [3]`output_path`.

For example:

`python play_with_gensim.py ../data/29.zip input.txt results_29.txt`

Precomputed results for the models `English Wikipedia (ID 200)` and `Gigaword (ID 29)` can be found at `./part1/`.

### Results

There are multiple differences between the associates list produced by the two models, ID200 and ID29. Firstly, the word tokens `current_ADV` and `parser_NOUN` were not available in the ID29 model. Thus, there were no associates listed for these tokens. The same holds for ID200 with the token `current_ADV`.

For the token `almost_ADV`, the two models perform similar. Both list `nearly_ADV` as the closest word to the input token `almost_ADV`, with similar cosine distances. For `dependency_NOUN`, however, the ID29 model returns words that altough they are semanticly similar, they have wery different word form. The ID200 model on the other hand, returns primarily morphologically similar tokens, words that are almost identical to the original input token. For example, where ID29 returns "Reliance" as the second closest neighbour to "dependency", ID200 returns "Dependencies", and this continues in similar manner throughout the list.

The models also return different results for the token `classify_VERB`. ID200 returns three verbs and two adjectives, while ID29 gives 4 adjectives and one verb. This indicate that the token "classify" has a rather different meaning in the corpus used to train ID200 (Wikipedia) than in ID29 (News articles). This matches perhaps the intution that "classify" is much more likely to appear as a way of describing a categorization process in a open resource dictionary than in a corpus of news articles, where one would expect it to be used in a similar fashion as "top-secret" and "confidential".

In short, domain specificity seems to influence the semantic relationship between words in the two models.

## Document classification with word embeddings

The experiments in this section utilised pretrained word2vec models to transform the input data into vector embeddings. The models were fetched from the NLPL model repository. The models used throughtout this report were:

- word2vec, tagged: id=200
- word2vec, untagged: id=12
- GLovE, tagged: id=13

We did not see the need to train our own word2vec model on the domain data. However, we decided to use a BERT embedding model which we allowed to fine-tune (see sections below).

### Experiment with different ways of creating fixed size representations of the sentences.

This section tries out different methods of creating fixed size representations of the input sentences. For the method `average`, we use the `torch.mean` function to create an average vector representation of all the input words per sequence. For the method `sum` we do likewise with summarization of the vectors.

The results of these experiments are reported as accuracy scores on a held out dev set, using a linear model on both a PoS-tagged and lemmatized version of the data. The model ran for 50 epochs in all cases, with a learning rate of 0.01 and a batch size of 64.

| Average | Sum   |Fixed size|
| ------- | ----- | ------ |
| 0.741   | 0.711 | 0.7349 |

As can be deduced from the table above, the `average` method offers the best performance in terms of accuracy.

### Experiment with different input methods

The following experiments train on different version of the original text: a raw representation, a Pos and Lemmatized representation and a purely lemmatized one, using a corresponding pre-trained embedding model from the NLPL repository (id in parenthsis). Model used: a dense linear model, with learning rate 0.01, on 50 epochs using the average method for fixed size vector representations.

| Raw (12) | PoS and Lemma (200) | Only Lemma |
| -------- | ------------------- | ---------- |
| 0.774    | 0.741               | 0.723      |

As can be seen from the table, the input representation without any additional tagging performs the best.

## Using RNNs

### Unidirectional:

|     | vanilla rnn | gru    | lstm   |
| --- | ----------- | ------ | ------ |
| w2v | 0.747       | 0.7467 | 0.7489 |

Below is a plot of the validation loss over time for the unidirectional RNN implemenations (RNN=green, LSTM=gray, GRU=orange)

![](img/rNN2.PNG)

### Bidirectional:

|     | vanilla rnn | gru   | lstm   |
| --- | ----------- | ----- | ------ |
| w2v | 0.74        | 0.753 | 0.7489 |

Below is a plot of the validation loss over time for the bidirectional RNN implemenations (RNN=red, LSTM=turquoise, GRU=pink)

![](img/rNN.PNG)

### Using BERT embeddings

We decided to experiment with the use of a more novel (2018) technique for generating word embeddings.
Namely Bidirectional Encoder Representations from Transformers (BERT). To compensate for the computational
expense ant train/inference time, we decided to use a lighter, but well perforing variant: MobileBERT
from the huggingface transformers library. We trained our GRU and LSTM implemtations on top of the
BERT vector representation. The training time increased up to 230 seconds per epoch, and it was apparent
that the model learned a lot from very few epochs.

**Fine-tuning MobileBERT**

When fine-tuning the model, to our surprise, the time for each epoch was about the same.  
The results were also very similar

| accuracies | BERT with LSTM | BERT with GRU |
| ---------- | -------------- | ------------- |
| Frozen     | 0.5            | 0.5           |
| Fine-tuned | Not tested     | 0.5           |

Note that we were not able to experiment substantially with this model so
we do not base the Conclusion on these results

# Conclusion

We were not able to find that RNNs give better results
than dense feed-forward neural networks. Our best model was the dense linear model, with an accuracy of 0.774.
