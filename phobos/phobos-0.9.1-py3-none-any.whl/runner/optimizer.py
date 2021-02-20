from torch.optim import (Adadelta, Adagrad, Adam, AdamW,
                         SparseAdam, Adamax, ASGD, LBFGS,
                         RMSprop, Rprop, SGD)

optimizer_map = {
    'adadelta': Adadelta,
    'adagrad': Adagrad,
    'adam': Adam,
    'adamw': AdamW,
    'sparseadam': SparseAdam,
    'adamax': Adamax,
    'asgd': ASGD,
    'lbfgs': LBFGS,
    'rmsprop': RMSprop,
    'rprop': Rprop,
    'sgd': SGD
}


def get_optimizer(key, args, model):
    optimizer = optimizer_map[key]
    args['params'] = model.parameters()
    return optimizer(**args)
