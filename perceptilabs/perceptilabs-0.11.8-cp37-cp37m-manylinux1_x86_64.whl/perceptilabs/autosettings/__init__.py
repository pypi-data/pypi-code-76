from perceptilabs.autosettings.base import SettingsEngine, InferenceRule
from perceptilabs.autosettings.rules import *


DEFAULT_RULES = [
    DeepLearningFcOutputShapeFromLabels,
    ProcessReshape1DFromPrimeFactors,
    DeepLearningConvDoubleFeatureMaps,
    DataDataShouldUseLazy
]


    
    
    
