import torch
from models import SingleLayerElmanRNN
from torch.nn import RNN

x = torch.randn(2, 4, 5)

rnn1 = RNN(5, 7)
rnn2 = SingleLayerElmanRNN(5, 7)

h1, y1 = rnn1(x)
h2, y2 = rnn2(x)
print(h1)
print(h2)
print(y1)
print(y2)
assert h1.shape == h2.shape, f"{h2.shape} != {h1.shape}"
assert y1.shape == y2.shape, f"{y2.shape} != {y1.shape}"
