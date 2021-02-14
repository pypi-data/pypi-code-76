import numpy
from deepleaps.dataloader.TensorTypes import *

"""
Basic transform methods
"""

class Transforms(object):
    def __init__(self, required=[], meta={}, output_name='{%s}'):
        self.required = required
        self.meta = meta
        if 'ALL' in self.meta.keys():
            for name in self.required:
                self.meta[name] = self.meta['ALL']
        self.output_name = output_name

    def output_format(self, input_name):
        return self.output_name.replace('{%s}', input_name)

class ToTensor(Transforms):
    def __init__(self, required=[], meta={}, output_name='{%s}'):
        super(ToTensor, self).__init__(required, meta)

    def __call__(self, samples):
        for sample in self.required:
            data = samples[sample]
            meta_data = self.meta[sample]

            if isinstance(meta_data, IMAGE):
                samples[self.output_format(sample)] = data.transpose((2, 0, 1))
            else:
                raise NotImplementedError
        return samples

class ToNumpy(Transforms):
    def __init__(self, required=[], meta={}, output_name='{%s}'):
        super(ToNumpy, self).__init__(required, meta, output_name)

    def __call__(self, samples):
        for sample in self.required:
            data = samples[sample]
            meta_data = self.meta[sample]
            if isinstance(meta_data, IMAGE):
                samples[self.output_format(sample)] = data.permute((0,2,3,1)).cpu().detach().numpy()
            else:
                raise NotImplementedError
        return samples
