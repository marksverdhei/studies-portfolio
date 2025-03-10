from .oblig1 import *

def plot_learning_curve(x, y, ylabel):
    plt.figure()
    plt.plot(x, y)

    plt.xlabel('Amount of training data')
    plt.ylabel(ylabel)

    if GUI:
        plt.show()
    else:
        save_plot("learning-curve")
