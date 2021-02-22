import matplotlib.pyplot as plt
import numpy as np


def plot(history):
    train_loss = history.history['loss']
    train_acc = history.history['accuracy']
    val_loss = history.history['val_loss']
    val_acc = history.history['val_accuracy']

    t = np.arange(0, len(train_loss), 1)
    fig, axs = plt.subplots(2, 1)

    color = 'tab:red'
    axs[0].set_xlabel('epoch')
    axs[0].set_ylabel('train_loss', color=color)
    axs[0].plot(t, train_loss, color=color)
    axs[0].tick_params(axis='y', labelcolor=color)

    ax12 = axs[0].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax12.set_ylabel('train_acc', color=color)  # we already handled the x-label with ax1
    ax12.plot(t, train_acc, color=color)
    ax12.tick_params(axis='y', labelcolor=color)

    color = 'tab:red'
    axs[1].set_xlabel('epoch')
    axs[1].set_ylabel('val_loss', color=color)
    axs[1].plot(t, val_loss, color=color)
    axs[1].tick_params(axis='y', labelcolor=color)

    ax22 = axs[1].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax22.set_ylabel('val_acc', color=color)  # we already handled the x-label with ax1
    ax22.plot(t, val_acc, color=color)
    ax22.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.show()
