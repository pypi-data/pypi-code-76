import torch

INPUT_SHAPE = (8, 8)
OUTPUT_SHAPE = (10,)

def feedforward_network(hidden_sizes, activation, last_layer_activation):
    layers = [torch.nn.Flatten()]
    if len(hidden_sizes) == 0:
        layers.append(torch.nn.Linear(INPUT_SHAPE[0] * INPUT_SHAPE[1],
                                      OUTPUT_SHAPE[0]))
        layers.append(last_layer_activation())
    else:
        for i in range(len(hidden_sizes)):
            if i == 0:
                layers.append(torch.nn.Linear(INPUT_SHAPE[0] * INPUT_SHAPE[1],
                                              hidden_sizes[0]))
            else:
                layers.append(torch.nn.Linear(hidden_sizes[i-1],
                                              hidden_sizes[i]))
            if i == len(hidden_sizes) - 1:
                layers.append(last_layer_activation())
            else:
                layers.append(activation())
    return torch.nn.Sequential(*layers)

def two_layer_sigmoid():
    return feedforward_network([30], torch.nn.Sigmoid, torch.nn.Sigmoid)
