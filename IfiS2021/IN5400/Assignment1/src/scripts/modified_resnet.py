from torchvision.models import resnet18
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from data_utils import VocDataset
import train
import logging

# renamed version of wsconv2
class WeightStandarizedConv2d(nn.Conv2d):
    def __init__(self, in_channels, out_channels, kernel_size, stride,
                 padding, dilation=1, groups=1, bias=None, eps=1e-12, parent=None):
        super(WeightStandarizedConv2d, self).__init__(in_channels, out_channels,
                                      kernel_size, stride, padding, dilation, groups, bias)
        self.eps = eps
        if parent != None:
            self._parameters = parent._parameters

    def forward(self, x):
        s = self.weight.std(axis=3, unbiased=False)
        W_hat = self.weight/(s**2+self.eps).sqrt()[:, :, :, None]
        output = F.conv2d(x, W_hat,
            bias=self.bias,
            stride=self.stride,
            padding=self.padding,
            dilation=self.dilation,
            groups=self.groups
        )

        return output


# class for modified resnet18 model
class WeightStandardizedResNet18(nn.Module):
    def __init__(self):
        super().__init__()
        self.base_model = resnet18()
        self._replace_conv_layers(self.base_model._modules)

    def _replace_conv_layers(self, modules):
        if len(modules): # not empty
            for k, v in modules.items():
                if isinstance(v, nn.Conv2d):
                    modules[k] = WeightStandarizedConv2d(
                        v.in_channels,
                        v.out_channels,
                        v.kernel_size,
                        v.stride,
                        v.padding,
                        v.dilation,
                        v.groups,
                        v.bias,
                        parent=v
                    )
                else:
                    self._replace_conv_layers(v._modules)

    def forward(self, x):
        return self.base_model(x)


def make_model(cuda=False, logits=False, freeze=True):
    model = WeightStandardizedResNet18()
    last_hidden_dim = model.base_model.fc.in_features

    if freeze:
        for param in model.parameters():
            param.requires_grad = False

    # overwrite last linear layer

    if logits:
        model.base_model.fc = nn.Linear(last_hidden_dim, train.NUMBER_OF_CLASSES)
    else:
        model.base_model.fc = nn.Sequential(
            nn.Linear(last_hidden_dim, train.NUMBER_OF_CLASSES),
            nn.Sigmoid()
        )

    if cuda:
        model = model.to("cuda")

    return model


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    model_path = "bin/modded_model_adam"
    train.make_model = make_model
    train.main({
        "root_dir": "/itf-fi-ml/shared/IN5400/dataforall/mandatory1/VOCdevkit/VOC2012/",
        "model_folder": model_path,
        "use_gpu": True,
        "lr": 0.005,
        "batchsize_train": 16,
        "batchsize_val": 64,
        "epochs": 5,
        "scheduler": None,
        "adam": True,
        "freeze": False,
        "seed": 42
    })
