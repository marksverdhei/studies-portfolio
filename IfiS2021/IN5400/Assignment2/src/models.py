from torch import nn
import torch.nn.functional as F
import torch
import numpy as np
from itertools import zip_longest

######################################################################################################################
class ImageCaptionModel(nn.Module):
    def __init__(self, config):
        super(ImageCaptionModel, self).__init__()
        """
        "ImageCaptionModel" is the main module class for the image captioning network

        Args:
            config: Dictionary holding neural network configuration

        Attributes:
            self.embedding   : An instance of nn.Embedding, shape[vocabulary_size, embedding_size]
            self.input_layer : An instance of nn.Linear, shape[number_of_cnn_features, hidden_state_sizes]
            self.rnn         : An instance of RNN
            self.outputlayer : An instance of nn.Linear, shape[hidden_state_sizes, vocabulary_size]
        """
        self.config = config
        self.vocabulary_size = config['vocabulary_size']
        self.embedding_size = config['embedding_size']
        self.number_of_cnn_features = config['number_of_cnn_features']
        self.hidden_state_sizes = config['hidden_state_sizes']
        self.num_rnn_layers = config['num_rnn_layers']
        self.cell_type = cell_type = config['cellType']
        self.nn_map_size = 512

        self.embedding = nn.Embedding(self.vocabulary_size, self.embedding_size)
        self.input_layer = nn.Sequential(
            nn.Dropout(p=0.25),
            nn.Linear(self.number_of_cnn_features, self.nn_map_size),
            nn.LeakyReLU()
        )

        num_rnn_layers = self.config['num_rnn_layers']
        rnn_input_size = self.embedding_size + self.nn_map_size
        simple_rnn = False

        use_custom_rnn = False

        if simple_rnn:
            assert self.cell_type == 'RNN'
            assert self.config['num_rnn_layers'] == 1

            self.rnn = SingleLayerElmanRNN(
                input_size=rnn_input_size,
                hidden_size=self.hidden_state_sizes
            )
        elif use_custom_rnn:
            self.rnn = RNN(
                input_size=rnn_input_size,
                hidden_size=self.hidden_state_sizes,
                num_layers=num_rnn_layers,
                cell_type=cell_type
            )
        else:
            BuiltinRNN = {
                    "RNN": nn.RNN,
                    "LSTM": nn.LSTM,
                    "GRU": nn.GRU
            }[cell_type]

            self.rnn = BuiltinRNN(
                    input_size=rnn_input_size,
                    hidden_size=self.hidden_state_sizes,
                    num_layers=num_rnn_layers
            )

        self.output_layer = nn.Linear(self.hidden_state_sizes, self.vocabulary_size)



    def forward(self, cnn_features, xTokens, is_train, current_hidden_state=None):
        """
        Args:
            cnn_features        : Features from the CNN network, shape[batch_size, number_of_cnn_features]
            xTokens             : Shape[batch_size, truncated_backprop_length]
                                  target tokens of an image captioning model used during training.
                                  (probably start token to, but excluding eos token)
            is_train            : "is_train" is a flag used to select whether or not to use estimated token as input
            current_hidden_state: If not None, "current_hidden_state" should be passed into the rnn module
                                  shape[num_rnn_layers, batch_size, hidden_state_sizes]

        Returns:
            logits              : Shape[batch_size, truncated_backprop_length, vocabulary_size]
            current_hidden_state: shape[num_rnn_layers, batch_size, hidden_state_sizes]
        """

        # Get "initial_hidden_state" shape[num_rnn_layers, batch_size, hidden_state_sizes].
        # Remember that each rnn cell needs its own initial state.
        print("tokens:", xTokens.shape)

        input_activations = self.input_layer(cnn_features).unsqueeze(1)
        # print(input_activations.shape)
        input_activations = input_activations.repeat(1, xTokens.shape[-1], 1)

        embeddings = self.embedding(xTokens)
        # print(input_activations.shape, embeddings.shape)
        initial_hidden_state = torch.cat((input_activations, embeddings), dim=-1)
        # print(initial_hidden_state.shape)

        # NOTE: RNN takes in two arguments:
        logits, current_hidden_state_out = self.rnn(initial_hidden_state, current_hidden_state)
        logits = self.output_layer(logits)

        return logits, current_hidden_state_out

######################################################################################################################


class SingleLayerElmanRNN(nn.Module):
    def __init__(self, input_size, hidden_size, activation_fn=torch.tanh):
        super(SingleLayerElmanRNN, self).__init__()

        self.input_size = input_size
        self.hidden_state_size = hidden_size

        self.cell = ElmanRNNCell(input_size, hidden_size, activation_fn=activation_fn)

    def forward(self, X, h=None):
        assert X.ndim == 3, "Input must be a 3-tensor"
        h = torch.stack([self.cell(x) for x in X], dim=0)
        return h, h[-1:, :, :]


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, cell_type='GRU'):
        super(RNN, self).__init__()
        """
        Args:
            input_size (Int)        : embedding_size
            hidden_state_size (Int) : Number of features in the rnn cells (will be equal for all rnn layers)
            num_rnn_layers (Int)    : Number of stacked rnns
            cell_type               : Whether to use vanilla or GRU cells

        Returns:
            self.cells              : A nn.ModuleList with entities of "RNNCell" or "GRUCell"
        """
        self.input_size = input_size
        self.hidden_state_size = hidden_size
        self.num_rnn_layers = num_layers
        self.cell_type = cell_type

        RNNCell = {
            "RNN": ElmanRNNCell,
            "LSTM": LSTMCell,
            "GRU": GRUCell
        }[cell_type]

        self.cells = torch.nn.ModuleList([RNNCell(input_size, hidden_size)] + [RNNCell(hidden_size, hidden_size) for i in range(self.num_rnn_layers-1)])
        assert len(self.cells) == self.num_rnn_layers

    def forward(self, X, h0):
        """
        Args:
            x
        Returns:
            logits        : The predicted logits. shape[batch_size, truncated_backprop_length, vocabulary_size]
            current_state : The hidden state from the last iteration (in time/words).
                            Shape[num_rnn_layers, batch_size, hidden_state_sizes]
        """
        outputs = []
        if h0 is not None and h0.ndim == 3:
            h0 = h0[:, -1, :]
        elif h0 is None:
            h0 = []

        for x, h0 in zip_longest(X, h0):
            for cell in self.cells:
                x = cell(x, h0)
            outputs.append(x)
        h = torch.stack(outputs, dim=0)
        return h, h[-1:, :, :]

########################################################################################################################

class ElmanRNNCell(nn.Module):
    def __init__(self, input_size, hidden_size, activation_fn=torch.tanh):
        super(ElmanRNNCell, self).__init__()
        """
        Args:
            input_size
            hidden_state_size
            activation_fn: tanh by default
        """
        self.hidden_state_size = hidden_size

        parameter_size = input_size + hidden_size

        weight_init = torch.randn(parameter_size, hidden_size) / np.sqrt(parameter_size)


        self.weight = nn.Parameter(weight_init)

        self.bias = nn.Parameter(torch.zeros(1, hidden_size))
        self.activation = activation_fn

    def forward(self, batch, h=None):
        """
        Args:
            batch: [batch_size, input_size]
            h: [batch_size, hidden_size]

        Returns:
            state_new: The updated hidden state of the recurrent cell. Shape [batch_size, hidden_state_sizes]
        """
        device = self.weight.device
        output_tensor = torch.empty(len(batch), self.hidden_state_size, dtype=batch.dtype).to(device)

        if h is None:
            h = torch.zeros(self.hidden_state_size).to(device)

        for i, x in enumerate(batch):
            inputs = torch.cat((x, h)).to(self.weight.device)
            h = self.activation(inputs @ self.weight + self.bias).squeeze()
            output_tensor[i] = h

        # In the elman rnn, the hidden representations and
        # outputs are the same
        return output_tensor


class GRUCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(GRUCell, self).__init__()
        """
        Args:
            hidden_state_size: Integer defining the size of the hidden state of rnn cell
            inputSize: Integer defining the number of input features to the rnn

        Returns:
            self.weight_u: A nn.Parameter with shape [hidden_state_sizes+inputSize, hidden_state_sizes]. Initialized using
                           variance scaling with zero mean.

            self.weight_r: A nn.Parameter with shape [hidden_state_sizes+inputSize, hidden_state_sizes]. Initialized using
                           variance scaling with zero mean.

            self.weight: A nn.Parameter with shape [hidden_state_sizes+inputSize, hidden_state_sizes]. Initialized using
                         variance scaling with zero mean.

            self.bias_u: A nn.Parameter with shape [1, hidden_state_sizes]. Initialized to zero.

            self.bias_r: A nn.Parameter with shape [1, hidden_state_sizes]. Initialized to zero.

            self.bias: A nn.Parameter with shape [1, hidden_state_sizes]. Initialized to zero.

        Tips:
            Variance scaling:  Var[W] = 1/n
        """
        self.concat_size = hidden_size+input_size

        self.hidden_state_size = hidden_size
        self.input_size = input_size

        self.weight_u = self.init_weights()
        self.bias_u = self.init_bias()

        self.weight_r = self.init_weights()
        self.bias_r = self.init_bias()

        self.weight = self.init_weights()
        self.bias = self.init_bias()


    def forward(self, batch, h=None):
        """
        Args:
            batch: tensor with shape [batch_size, inputSize]
            state_old: tensor with shape [batch_size, hidden_state_sizes]

        Returns:
            state_new: The updated hidden state of the recurrent cell. Shape [batch_size, hidden_state_sizes]

        """
        device = self.weight.device

        output_tensor = torch.empty(len(batch), self.hidden_state_size, dtype=batch.dtype).to(device)

        if h is None:
            h = torch.zeros(self.hidden_state_size).to(device)

        for i, x in enumerate(batch):
            xh = torch.cat((x, h))
            xh_r = torch.sigmoid(xh @ self.weight_r + self.bias_r).squeeze()

            xh2 = torch.cat((x, (xh_r * h)))

            h_tilde = torch.tanh(xh2 @ self.weight + self.bias)

            xh_u = torch.sigmoid(xh @ self.weight_u + self.bias_u)

            hu = h * xh_u

            h = hu + (1-xh_u) * h_tilde
            h = h.squeeze()
            output_tensor[i] = h
        return output_tensor

    def init_weights(self):
        w = torch.randn(self.concat_size, self.hidden_state_size)
        return nn.Parameter(w * w.var())

    def init_bias(self):
        return nn.Parameter(torch.zeros(1, self.hidden_state_size))
######################################################################################################################


######################################################################################################################


class LSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(LSTMCell, self).__init__()
        """
        Args:
            hidden_state_size: Integer defining the size of the hidden state of rnn cell
            inputSize: Integer defining the number of input features to the rnn

            note: the actual tensor has 2*hidden_state_size because it contains hiddenstate and memory cell
        Returns:
            self.weight_f ...

        Tips:
            Variance scaling:  Var[W] = 1/n
        """
        self.concat_size = hidden_size+input_size

        self.hidden_state_size = hidden_size
        self.input_size = input_size

        self.weight_f = self.init_weights()
        self.bias_f = self.init_bias()

        self.weight_i = self.init_weights()
        self.bias_i = self.init_bias()

        self.weight_meminput = self.init_weights()
        self.bias_meminput = self.init_bias()

        self.weight_o = self.init_weights()
        self.bias_o = self.init_bias()



    def forward(self, batch, h=None):
        """
        Args:
            x: tensor with shape [batch_size, inputSize]
            state_old: tensor with shape [batch_size, 2*hidden_state_sizes]

        Returns:
            state_new: The updated hidden state of the recurrent cell. Shape [batch_size, hidden_state_sizes]

        """
        device = self.weight_f.device

        output_tensor = torch.empty(len(batch), self.hidden_state_size, dtype=batch.dtype).to(device)

        # How is this initialized?
        c = torch.zeros(self.hidden_state_size).to(device)

        if h is None:
            h = torch.zeros(self.hidden_state_size).to(device)


        for i, x in enumerate(batch):
            x_h = torch.cat((x, h))
            # linears
            f_state = torch.sigmoid(x_h @ self.weight_f + self.bias_f).squeeze()
            i_state = torch.sigmoid(x_h @ self.weight_i + self.bias_i).squeeze()
            c_canidate = torch.tanh(x_h @ self.weight_meminput + self.bias_meminput).squeeze()
            o_state = torch.sigmoid(x_h @ self.weight_o + self.bias_o).squeeze()

            # memory
            c *= f_state
            c += i_state * c_canidate

            h = o_state * torch.tanh(c)

            output_tensor[i] = h

        return output_tensor

    def init_weights(self):
        w = torch.randn(self.concat_size, self.hidden_state_size)
        return nn.Parameter(w * w.var())

    def init_bias(self):
        return nn.Parameter(torch.zeros(1, self.hidden_state_size))


######################################################################################################################
def loss_fn(logits, yTokens, yWeights):
    """
    Weighted softmax cross entropy loss.

    Args:
        logits          : shape[batch_size, truncated_backprop_length, vocabulary_size]
        yTokens (labels): Shape[batch_size, truncated_backprop_length]
        yWeights        : Shape[batch_size, truncated_backprop_length]. Add contribution to the total loss only from words exsisting
                          (the sequence lengths may not add up to #*truncated_backprop_length)

    Returns:
        sumLoss: The total cross entropy loss for all words
        meanLoss: The averaged cross entropy loss for all words

    Tips:
        F.cross_entropy
    """
    eps = 0.0000000001  # used to not divide on zero

    logits = logits.view(-1, logits.shape[2])
    yTokens = yTokens.view(-1)
    yWeights = yWeights.view(-1)
    losses = F.cross_entropy(input=logits, target=yTokens, reduction='none')

    sumLoss = (losses*yWeights).sum()
    meanLoss = sumLoss / (yWeights.sum()+eps)

    return sumLoss, meanLoss


# ########################################################################################################################
# if __name__ == '__main__':
#
#     lossDict = {'logits': logits,
#                 'yTokens': yTokens,
#                 'yWeights': yWeights,
#                 'sumLoss': sumLoss,
#                 'meanLoss': meanLoss
#     }
#
#     sumLoss, meanLoss = loss_fn(logits, yTokens, yWeights)
#
