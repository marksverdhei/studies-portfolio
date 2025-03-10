# Find out:

Kl divergence: how do does it relate to bayesian dl and differentiation

kl divergence is a way to compare probability distributions

MANN: Memory Augmented Neural Network

### Datasets

Train and test set distribution should rely on the size of the dataset.

For dev and test sets, absolute volume of data is more important, so if the dataset is large enough, 98% of the data could be of training

For small datasets, 70-30 or similar can suffice


### CNNS

#### Translational Invariance vs Equivariance

Invariance: when an image is shifted by some pixels, the activations stay the same (as long as the classification object is still present)
Equivariance: when an image is shifted by some pixels, the activations are shifted the same way

#### Rotation equivariant models

Cnn layers with kernels rotated to produce equivariance: deep rotation equivariant network


#### Formula for output shape of cnn layer  

if height = width

```
width + (2 * pad_size) - kernel_size
____________________________________

             stride
```

### Pooling

Types of pooling:
max, min, sum, avg/mean

why does max pooling work:

for relu networks, a large number means that the model has detected a feature (importance based on magnitude)
Nobody knows exactly why, but it has shown good results empirically


### RNNs

Decoder-encoder model

For machine translation, the encode encodes the sentence into a hidden state that works as a sentence embedding as input for the decoder. All is optimized for the task, so the embedding will be task specific
 
#### Bahdanau attention  

![](https://www.youtube.com/watch?v=B3uws4cLcFw)

For rnn encoder models, attention is used to remember long term dependencies in sequence data

rnn attention is quadratic in time complexity because you must compute the attention of the decoder with every state of the decoder
O(nm) where n = number of encoder states and m = number of decoder states

the attention activations are computed using it's own set of weights. The activations are normalized using the softmax function so they add up to 1

align function:

a* = v.T @ tanh(W @ concat(hi, s0))

[a1, a2, a3, ai] = Softmax([a*1, a*2, a*3, a*i])

c0 weighted average of the encoder states with the attention "weights" (not trainable params, but output of the attention components)

for each output, compute
align(hj, si)

#### Hard vs soft attention: 

Soft attention is just what we described, taking a weighted average of all the hidden states to create a context (different from lstm context)

In hard attention, we produce the "weights" and randomly select one hidden state from the softmax distribution
Sampling is not differentiable, so you cannot backpropagate normally

#### Attention in image captioning

The attention network takes each image feature map as a vector so that the model can attend to the different locations (e.g. each pixel or square of pixels) in the image. After, the weighted average can be passed through an MLP etc..
Image attention is easy to visualize

