import yaml

DEFAULT = {
    'val_ratio': 0.2,
    'augmentations': 'basic',
    'no_shuffle': False,
    'model': 'efficientnet-b0', # 'mobilenet_v2',
    'no_pretrained': False,
    'batch_size': 8,
    'epochs': 2,
    'criterion': 'bce', # 'crossentropy',
    'optimizer': 'adam',
    'automatic_optimization': False,
    'lr': 0.01,
    'momentum': 0.9,
    'betas': (0.9, 0.99),
    'weight_decay': 0,
    'monitor': 'val/loss',
    'early_stop': 0,
    'patience': 5,
    'num_workers': 6,
    'cpu': False,
    'half_precision': False,
    'seed': None,
    'tracking_uri': 'sqlite:///mlruns.db',
    'experiment_name': 'Default',
    'run_name': 'noname',
    'user': None,
    'tensorboard': False,
    'silence': False,
}

def generate_default_parameters(path='./default.yaml'):
    with open(path, 'w') as f:
        yaml.dump(DEFAULT, f, allow_unicode=True)
