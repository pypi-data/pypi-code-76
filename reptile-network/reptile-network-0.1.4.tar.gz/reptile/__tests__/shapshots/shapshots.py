import os
from ...Network.Network import Network
from ...Core.Core import core

dirname = os.path.dirname(__file__)
test_file = f'{dirname}/test_snapshot.json'


def setup(console = False):
    input_arrange = core.random.uniform(0, 1, 784)

    net1 = Network() \
        .input(784) \
        .layer(516) \
        .layer(128) \
        .layer(32) \
        .layer(10) \

    net1_output = net1.feed(input_arrange)
    net1.dumps(test_file)

    net2 = Network()
    net2.loads(file_path=test_file)
    os.remove(test_file)

    if console:
        print('Net 1:')
        print(net1)

        print('Net 2:')
        print(net2)

    net2_output = net2.feed(input_arrange)

    if repr(net1) != repr(net2):
        raise Exception('Nets are different')

    if not (net1_output == net2_output).all():
        raise Exception('Outputs are different')
