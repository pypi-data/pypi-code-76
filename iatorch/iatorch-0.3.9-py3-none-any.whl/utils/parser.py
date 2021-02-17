import torch.nn as nn
import torchvision.models as models
from efficientnet_pytorch import EfficientNet
from ..config.availables import MODELS, CRITERIONS, OPTIMIZERS, METRICS, AUGMENTATIONS


################################################################################################################################
# parser: criterion, model, optimizer, metric
################################################################################################################################

################################################################
# prep_args
################################################################
def prep_args(s):
    if s is not None:
        for _r in ['_', '-', ]:
            s = s.replace(_r, '')
        s = s.lower()
    return s

################################################################
# parse_criterion
################################################################
def criterion(criterion):
    criterion_ = prep_args(criterion)
    loss_function = None
    for lf, spec in CRITERIONS.items():
        if criterion_ in spec['names']:
            loss_function = spec['loss_function']
            break
    if loss_function is None:
        raise ValueError(f"Criterion '{criterion}' is not available.")
    return loss_function

################################################################
# parse_binary
################################################################
def is_binary(criterion):
    criterion_ = prep_args(criterion)
    is_binary_ = False
    if criterion_ is not None:
        for lf, spec in CRITERIONS.items():
            if criterion_ in spec['names']:
                is_binary_ = spec['is_binary']
                break
    return is_binary_

################################################################
# parse_optimizer
################################################################
def optimizer(optimizer, **kwargs):
    '''
    Parameters
    ----------
    optimizer : string
        Name of optimizer
    lr, momentum, betas, weight_decay : float, float, tuple(float, float), float
        paramters for optimizer
        
    Ruturns
    -------
    Optimizer, opt_params - NOTE! Optimizer is class not a function
    '''
    optimizer_ = prep_args(optimizer)
    Optimizer, optim_params = None, None
    for _, spec in OPTIMIZERS.items():
        if optimizer_ in spec['names']:
            Optimizer, optim_params = spec['class'], spec['params']
            break
    if Optimizer is None:
        raise ValueError(f"Optimizer '{optimizer}' is not available")
    optim_params = {k: v for k, v in kwargs.items() if k in optim_params and v is not None}
    return Optimizer, optim_params

################################################################
# parse_model
################################################################
def model(model_name, num_classes=None, pretrained=False):
    '''
    '''
    # model
    if 'efficientnet' in prep_args(model_name):
        if pretrained:
            model = EfficientNet.from_pretrained(model_name)
        else:
            model = EfficientNet.from_name(model_name)        
    else:
        model = eval(f'models.{model_name}(pretrained={pretrained})')
    
    # modify classifier
    if num_classes is not None:
        classifier = getattr(model, MODELS[model_name]['classifier'])
        if isinstance(classifier, nn.modules.container.Sequential):
            in_features = classifier[-1].in_features
            classifier[-1] = nn.Linear(in_features, num_classes)
        else:
            in_features = classifier.in_features
            setattr(model, MODELS[model_name]['classifier'], nn.Linear(in_features, num_classes))
        
    return model

################################################################
# parse_metric
################################################################
def metric(metric_name, num_classes, is_binary, **kwargs):
    '''
    metric parser using pre-defined availables
    '''
    metric_ = prep_args(metric_name)
    Metric, metric_params = None, None
    for _, spec in METRICS.items():
        if metric_ in spec['names']:
            Metric, metric_params = spec['class'], spec['params']
            break
    if Metric is None:
        raise ValueError(f"Metric '{metric_name}' is not available")
    kwargs.update({'num_classes': num_classes, 'multilabel': is_binary and (num_classes > 1)})
    kwargs = {
        k: v for k, v in kwargs.items() if k in metric_params
    }
    return Metric(compute_on_step=False, **kwargs)    # compute_on_step=False,


################################################################
# augmentations
################################################################
def augmentations(list_transforms):
    
    if not isinstance(list_transforms, list):
        if list_transforms == 'basic':
            list_transforms = ['Normailize', 'Flip', 'ColorJitter', 'GaussNoise', 'ISONoise', ]
        else:
            list_transforms = [list_transforms]
    
    return [v() for k, v in AUGMENTATIONS.items() if k.lower() in [e.lower() for e in list_transforms]]
