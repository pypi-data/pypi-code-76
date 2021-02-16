import os
import idx2numpy
from ...Network.Network import Network
from ...Core.Core import core

dirname = os.path.dirname(__file__)
dataset_file = f'{dirname}/train-images.idx3-ubyte'
labels_file = f'{dirname}/train-labels.idx1-ubyte'


def setup(console = False):
    arr = core.array(idx2numpy.convert_from_file(dataset_file))
    labels_arr = core.array(idx2numpy.convert_from_file(labels_file))
    arr_flatened = core.array([item.reshape((1, 784))[0] / 255 for item in arr])

    diagonal = core.eye(10)
    labels_masks = core.array([diagonal[i] for i in labels_arr])

    net = Network() \
        .input(784) \
        .layer(516) \
        .layer(128) \
        .layer(32) \
        .layer(10) \

    net.fit(
        arr_flatened[:50000],
        labels_masks[:50000],
        batch_size=10,
        learning_const=0.1,
        epochs=15,
        console=console
    )

    counter = 0
    for sample, label in zip(arr_flatened[50000:], labels_masks[50000:]):
        answer = net.feed(core.array([sample])).round()
        if (answer == label).all():
            counter += 1

    result = counter / len(arr_flatened[50000:])

    if console:
        print(result)

    if result < 0.93:
        raise Exception('Not enough accuracy')


if __name__ == '__main__':
    setup(True)
