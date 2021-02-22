from medpy.metric.binary import dc
import numpy as np
from medpy.metric.binary import sensitivity as medsensitivity
from medpy.metric.binary import jc
from medpy.metric.binary import positive_predictive_value

class Segmentation:
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

    def dice(self):
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
            dsc = dc(gt_c_i, pred_c_i)
            res.append(dsc)
        return res

    def sensitivity(self):
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
            sen = medsensitivity(gt_c_i, pred_c_i)
            res.append(sen)
        return res
    
    def jaccard(self):
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
            jac = jc(gt_c_i, pred_c_i)
            res.append(jac)
        return res

    def ppv(self):
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
            pp = positive_predictive_value(gt_c_i, pred_c_i)
            res.append(pp)
        return res
    