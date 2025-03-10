import matplotlib as mpl
import matplotlib.pyplot as plt
import torch
import numpy as np

model_path = "bin/bin/default_model_adam/model_epoch11.pt"

def main():
    mpl.style.use("ggplot")
    device = torch.device("cpu")
    model_dict = torch.load(model_path, map_location=device)
    train_losses = model_dict["train_loss"]
    val_losses = model_dict["val_loss"]
    epochs = np.arange(len(train_losses))+1
    plt.plot(epochs, train_losses, label="train set", c="blue")
    plt.plot(epochs, val_losses, label="validation set", c="orange")
    # plt.grid()
    plt.title("Losses over epochs during training")
    plt.ylabel("cross entropy loss")
    plt.xlabel("epoch")
    plt.legend()
    plt.show()

    map_scores = model_dict["map_score"]
    plt.plot(epochs, map_scores, label="Mean AP score", c="orange")
    # plt.grid()
    plt.title("AP scores on dev set over epochs during training")
    plt.ylabel("AP")
    plt.xlabel("epoch")
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()
