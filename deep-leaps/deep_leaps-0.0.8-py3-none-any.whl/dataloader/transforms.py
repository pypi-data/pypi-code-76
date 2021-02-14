import numpy
from deepleaps.dataloader.TensorTypes import *

"""
Basic transform methods
"""
class Transforms(object):
    def __init__(self, required: list, output_name='{%s}'):
        self.required = required
        self.output_name = output_name

    def output_format(self, input_name):
        return self.output_name.replace('{%s}', input_name)

class ToTensor(Transforms):
    def __init__(self, required: list, output_name='{%s}'):
        super(ToTensor, self).__init__(required)

    def __call__(self, samples):
        for sample in self.required:
            data = samples[sample]
            samples[self.output_format(sample)] = data.transpose((2, 0, 1))
        return samples

class ToNumpy(Transforms):
    def __init__(self, required: list, output_name='{%s}'):
        super(ToNumpy, self).__init__(required, output_name)

    def __call__(self, samples):
        for sample in self.required:
            data = samples[sample]
            samples[self.output_format(sample)] = data.permute((0,2,3,1)).cpu().detach().numpy()
        return samples
