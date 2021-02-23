from torch.optim.lr_scheduler import (MultiplicativeLR, StepLR,
                                      LambdaLR, MultiStepLR, ExponentialLR,
                                      ReduceLROnPlateau, CyclicLR,
                                      OneCycleLR, CosineAnnealingWarmRestarts)

scheduler_map = {
    'multiplicative': MultiplicativeLR,
    'step': StepLR,
    'lmbda': LambdaLR,
    'multistep': MultiStepLR,
    'exponential': ExponentialLR,
    'plateau': ReduceLROnPlateau,
    'cyclic': CyclicLR,
    'one_cycle': OneCycleLR,
    'cos_anneal': CosineAnnealingWarmRestarts
}


def get_scheduler(key, args, optimizer):
    scheduler = scheduler_map[key]
    args['optimizer'] = optimizer
    return scheduler(**args)
