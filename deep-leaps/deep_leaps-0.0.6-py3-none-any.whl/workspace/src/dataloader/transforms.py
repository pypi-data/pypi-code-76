from deepleaps.dataloader.Transform import TRANSFORM, Transforms
from deepleaps.dataloader.TensorTypes import IMAGE

class ToNumpy(Transforms):
    def __init__(self, required=[], meta={}):
        super(ToNumpy, self).__init__(required, meta)

    def __call__(self, samples):
        for sample in self.required:
            data = samples[sample]
            meta_data = self.meta[sample]
            if isinstance(meta_data, IMAGE):
                samples[sample] = data.permute((0,2,3,1)).cpu().detach().numpy()
            else:
                raise NotImplementedError
        return samples

# make transform class, and you must to TRANSFORM.transform
TRANSFORM['ToNumpy'] = ToNumpy
