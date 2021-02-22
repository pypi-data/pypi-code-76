import numpy as np
from skimage.measure import compare_ssim
from skimage.measure import compare_psnr


class Synthesis:
    def __init__(self, test, pred, classes):
        if '.npy' in test:
            self.test = np.load(test)
        else:
            self.test = test
        if '.npy' in pred:
            self.pred = np.load(pred)
        else:
            self.pred = pred
        self.classes = classes
        
    def mse(self):
        if self.test.ndim != self.pred.ndim:
            raise ValueError("The arrays 'test' and 'pred' should have the "
                             "same dimension, {} against {}".format(self.test.ndim,
                                                                    self.pred.ndim))
        res = []
        for c in range(1, self.classes):
            gt_c_i = np.copy(self.test)
            gt_c_i[gt_c_i != c] = 0
            pred_c_i = np.copy(self.pred)
            pred_c_i[pred_c_i != c] = 0
            gt_c_i = np.clip(gt_c_i, 0, 1)
            pred_c_i = np.clip(pred_c_i, 0, 1)
            se = np.mean((gt_c_i - pred_c_i) ** 2.)
            res.append(se)
        return res

    def ssim(self):
        if self.test.ndim != self.pred.ndim:
            raise ValueError("The arrays 'test' and 'pred' should have the "
                             "same dimension, {} against {}".format(self.test.ndim,
                                                                    self.pred.ndim))
        res = []
        for c in range(1, self.classes):
            gt_c_i = np.copy(self.test)
            gt_c_i[gt_c_i != c] = 0
            pred_c_i = np.copy(self.pred)
            pred_c_i[pred_c_i != c] = 0
            gt_c_i = np.clip(gt_c_i, 0, 1)
            pred_c_i = np.clip(pred_c_i, 0, 1)
            sm = compare_ssim(gt_c_i - pred_c_i)
            res.append(sm)
        return res
    
    def psnr(self):
        if self.test.ndim != self.pred.ndim:
            raise ValueError("The arrays 'test' and 'pred' should have the "
                             "same dimension, {} against {}".format(self.test.ndim,
                                                                    self.pred.ndim))
        res = []
        for c in range(1, self.classes):
            gt_c_i = np.copy(self.test)
            gt_c_i[gt_c_i != c] = 0
            pred_c_i = np.copy(self.pred)
            pred_c_i[pred_c_i != c] = 0
            gt_c_i = np.clip(gt_c_i, 0, 1)
            pred_c_i = np.clip(pred_c_i, 0, 1)
            dr = np.max([pred_c_i.max(), gt_c_i.max()]) - np.min([pred_c_i.min(), gt_c_i.min()])
            nr = compare_psnr(gt_c_i - pred_c_i, dr)
            res.append(nr)
        return res
