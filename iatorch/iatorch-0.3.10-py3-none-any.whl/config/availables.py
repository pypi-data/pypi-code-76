import torch.nn as nn
import torch.optim as optim
from pytorch_lightning import metrics
from iautils.image import transforms as T


################################################################################################################################
# EXTENSIONS
################################################################################################################################
EXTENSIONS = {'audio': ['wav', 'tdms', 'mp3'], 'image': ['png', 'jpg', 'gif', 'bmp'], }
EXTENSIONS['all'] = [extension for extensions in EXTENSIONS.values() for extension in extensions]


################################################################################################################################
# MODELS
################################################################################################################################
MODELS = {
    'efficientnet-b0': {
        'input_shape': (224, 224, 3), 'parameters': '5.3M', 'top_1_acc': '76.3%',
        'classifier': '_fc',
    },
    'efficientnet-b1': {
        'input_shape': (224, 224, 3), 'parameters': '7.8M', 'top_1_acc': '78.8%',
        'classifier': '_fc',
    },
    'efficientnet-b2': {
        'input_shape': (224, 224, 3), 'parameters': '9.2M', 'top_1_acc': '79.8%',
        'classifier': '_fc',
    },
    'efficientnet-b3': {
        'input_shape': (224, 224, 3), 'parameters': '12M', 'top_1_acc': '81.1%',
        'classifier': '_fc',
    },
    'efficientnet-b4': {
        'input_shape': (224, 224, 3), 'parameters': '19M', 'top_1_acc': '82.6%',
        'classifier': '_fc',
    },
    'efficientnet-b5': {
        'input_shape': (224, 224, 3), 'parameters': '30M', 'top_1_acc': '83.3%',
        'classifier': '_fc',
    },
    'efficientnet-b6': {
        'input_shape': (224, 224, 3), 'parameters': '43M', 'top_1_acc': '84.0%',
        'classifier': '_fc',
    },
    'efficientnet-b7': {
        'input_shape': (224, 224, 3), 'parameters': '66M', 'top_1_acc': '84.4%',
        'classifier': '_fc',
    },
    'alexnet': {
        'input_shape': (256, 256, 3), 'parameters': '60M', 'top_1_acc': '63.3%',
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'densenet121': {
        'input_shape': (224, 224, 3), 'parameters': '8M', 'top_1_acc': '74.5%',
        'classifier': 'classifier',
    },
    'densenet161': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier',
    },
    'densenet169': {
        'input_shape': (224, 224, 3), 'parameters': '14M', 'top_1_acc': '75.9%',
        'classifier': 'classifier',
    },
    'densenet201': {
        'input_shape': (224, 224, 3), 'parameters': '20M', 'top_1_acc': '77.0%',
        'classifier': 'classifier',
    },
    'googlenet': {
        'input_shape': (224, 224, 3), 'parameters': '23M', 'top_1_acc': '74.8%',
        'classifier': 'fc',
    },
    'inception_v3': {
        'input_shape': (299, 299, 3), 'parameters': '23.8M', 'top_1_acc': '78.0%',
        'classifier': 'fc',
    },
    
    'mobilenet_v2': {
        'input_shape': (224, 224, 3), 'parameters': '3.47M', 'top_1_acc': '71.9%',
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'resnet50': {
        'input_shape': (224, 224, 3), 'parameters': '25.6M', 'top_1_acc': '75.2%',
        'classifier': 'fc',
    },
    'resnet101': {
        'input_shape': (224, 224, 3), 'parameters': '45M', 'top_1_acc': '76.4%',
        'classifier': 'fc',
    },
    'resnet152': {
        'input_shape': (224, 224, 3), 'parameters': '60M', 'top_1_acc': '77.8%',
        'classifier': 'fc',
    },
    'resnet18': {
        'input_shape': (224, 224, 3), 'parameters': '11.7M', 'top_1_acc': '70.4%',
        'classifier': 'fc',
    },
    'resnet34': {
        'input_shape': (224, 224, 3), 'parameters': '21.8M', 'top_1_acc': '73.3%',
        'classifier': 'fc',
    },
    'mnasnet0_5': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier',
    },
    'mnasnet0_75': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier',
    },
    'mnasnet1_0': {
        'input_shape': (224, 224, 3), 'parameters': '4.2M', 'top_1_acc': '74.0%',
        'classifier': 'classifier',
    },
    'mnasnet1_3': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier',
    },
    'vgg11': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg11_bn': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg13': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg13_bn': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg16': {
        'input_shape': (224, 224, 3), 'parameters': '138M', 'top_1_acc': '71.5%',
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg16_bn': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg19': {
        'input_shape': (224, 224, 3), 'parameters': '143M', 'top_1_acc': '71.1%',
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'vgg10_bn': {
        'input_shape': (224, 224, 3),
        'classifier': 'classifier', # nn.modules.container.Sequential
    },
    'wide_resnet50_2': {
        'input_shape': (32, 32, 3),
        'classifier': 'fc',
    },
    'wide_resnet101_2': {
        'input_shape': (32, 32, 3),
        'classifier': 'fc',
    },
}


################################################################################################################################
# CRITERIONS
################################################################################################################################
CRITERIONS = {
    'CrossEntropyLoss': {
        'names': ['crossentropy', 'crossentropy', 'crossentropyloss'],
        'loss_function': nn.CrossEntropyLoss(),
        'is_binary': False,
    },
    # Binary CrossEntropy는 기본적으로 WithLogitsLoss를 사용 - model module의 consistency를 위해서
    'BCEWithLogitsLoss': {
        'names': ['bce', 'binarycrossentropy', 'onevsall'],
        'loss_function': nn.BCEWithLogitsLoss(),
        'is_binary': True,
    },
}


################################################################################################################################
# OPTIMIZERS
################################################################################################################################
OPTIMIZERS = {
    'Adam': {
        'names': ['adam'],
        'class': optim.Adam,
        'params': ['lr', 'betas', 'weight_decay'],
    },
    'AdamW': {
        'names': ['adamw'],
        'class': optim.AdamW,
        'params': ['lr', 'betas', 'weight_decay'], 
    },
    'SparseAdam': {
        'names': ['sparseadam'],
        'class': optim.SparseAdam,
        'params': ['lr', 'betas', 'weight_decay'], 
    },
    'SGD': {
        'names': ['sgd'],
        'class': optim.SGD,
        'params': ['lr', 'momentum', 'weight_decay'],
    },
}


################################################################################################################################
# MATRICS
################################################################################################################################
METRICS = {
    'Accuracy': {
        'names': ['accuracy', 'acc'],
        'class': metrics.Accuracy,
        'params': ['threshold'],
    },
    'AveragePrecision': {
        'names': ['averageprecision', 'avgprecision'],
        'class': metrics.AveragePrecision,
        'params': ['num_classes', 'pos_label'],
    },
    'ConfusionMatrix': {
        # can not be direct logged - artifact로 저장할 것
        'names': ['confusionmatrix', 'cm', 'confmat'],
        'class': metrics.ConfusionMatrix,
        'params': ['num_classes', 'threshold', 'normalize'],
    },
    'F1': {
        'names': ['f1'],
        'class': metrics.F1,
        'params': ['num_classes', 'threshold', 'average', 'multilabel'],    # multilabel을 self.binary에서 받아올 것
    },
    'FBeta': {
        'names': ['fbeta'],
        'class': metrics.FBeta,
        'params': ['num_classes', 'beta', 'threshold', 'average', 'multilabel'],
    },
    'Precision': {
        'names': ['precision'],
        'class': metrics.Precision,
        'params': ['num_classes', 'threshold', 'average', 'multilabel'],
    },
    'PrecisionRecallCurve': {
        'names': ['precisionrecallcurve', 'curve', 'prcurve'],
        'class': metrics.PrecisionRecallCurve,
        'params': ['num_classes', 'pos_label'],
    },
    'Recall': {
        'names': ['recall'],
        'class': metrics.Recall,
        'params': ['num_classes', 'threshold', 'average', 'multilabel'],
    },
    'ROC': {
        'names': ['roc'],
        'class': metrics.ROC,
        'params': ['num_classes', 'pos_label'],
    },
}


################################################################################################################################
# TRANSFORMS
################################################################################################################################
AUGMENTATIONS = {
    "Blur": T.Blur,
    "VerticalFlip": T.VerticalFlip,
    "HorizontalFlip": T.HorizontalFlip,
    "Flip": T.Flip,
    "Normalize": T.Normalize,
    "Transpose": T.Transpose,
    "RandomGamma": T.RandomGamma,
    "OpticalDistortion": T.OpticalDistortion,
    "GridDistortion": T.GridDistortion,
    "RandomGridShuffle": T.RandomGridShuffle,
    "HueSaturationValue": T.HueSaturationValue,
    "PadIfNeeded": T.PadIfNeeded,
    "RGBShift": T.RGBShift,
    "RandomBrightness": T.RandomBrightness,
    "RandomContrast": T.RandomContrast,
    "MotionBlur": T.MotionBlur,
    "MedianBlur": T.MedianBlur,
    "GaussianBlur": T.GaussianBlur,
    "GaussNoise": T.GaussNoise,
    "GlassBlur": T.GlassBlur,
    "CLAHE": T.CLAHE,
    "ChannelShuffle": T.ChannelShuffle,
    "InvertImg": T.InvertImg,
    "ToGray": T.ToGray,
    "ToSepia": T.ToSepia,
    "JpegCompression": T.JpegCompression,
    "ImageCompression": T.ImageCompression,
    "Cutout": T.Cutout,
    "CoarseDropout": T.CoarseDropout,
    "ToFloat": T.ToFloat,
    "FromFloat": T.FromFloat,
    "RandomBrightnessContrast": T.RandomBrightnessContrast,
    "RandomSnow": T.RandomSnow,
    "RandomRain": T.RandomRain,
    "RandomFog": T.RandomFog,
    "RandomSunFlare": T.RandomSunFlare,
    "RandomShadow": T.RandomShadow,
    "Lambda": T.Lambda,
    "ChannelDropout": T.ChannelDropout,
    "ISONoise": T.ISONoise,
    "Solarize": T.Solarize,
    "Equalize": T.Equalize,
    "Posterize": T.Posterize,
    "Downscale": T.Downscale,
    "MultiplicativeNoise": T.MultiplicativeNoise,
    "FancyPCA": T.FancyPCA,
    "MaskDropout": T.MaskDropout,
    "GridDropout": T.GridDropout,
    "ColorJitter": T.ColorJitter,
#     "Sharpen": T.Sharpen,
#     "Emboss": T.Emboss,
}
