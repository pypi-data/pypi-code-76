from deepleaps.dataloader.Transform import TRANSFORM, Transforms
from deepleaps.dataloader.TensorTypes import IMAGE

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

import inspect, sys
for class_name, module in inspect.getmembers(sys.modules[__name__], inspect.isclass):
    if module.__module__ is not __name__: continue
    TRANSFORM[class_name] = module
