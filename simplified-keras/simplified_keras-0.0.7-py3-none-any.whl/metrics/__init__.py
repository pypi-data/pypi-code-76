import tensorflow as tf
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os


def get_confusion_matrixes(predicted_classes, labels):
    cm= tf.math.confusion_matrix(labels=labels, predictions=predicted_classes).numpy()
    cm_normalized= np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)
    return cm, cm_normalized


def get_model_statistics(confusion_matrix):
    class Stats:
        def __init__(self):
            self.FP = confusion_matrix.sum(axis=0) - np.diag(confusion_matrix)
            self.FN = confusion_matrix.sum(axis=1) - np.diag(confusion_matrix)
            self.TP = np.diag(confusion_matrix)
            self.TN = confusion_matrix.sum() - (self.FP + self.FN + self.TP)
            tp_fn_sum = self.TP + self.FN
            tn_fp_sum = self.TN + self.FP
            tp_fp_sum = self.TP + self.FP
            tn_fn_sum = self.TN + self.FN
            all_sum = tp_fp_sum + tn_fn_sum
            # Sensitivity/true positive rate
            self.TPR = self.TP / tp_fn_sum
            self.TPR[np.isnan(self.TPR)] = 0
            # Specificity/true negative rate
            self.TNR = self.TN / tn_fp_sum
            self.TNR[np.isnan(self.TNR)] = 0
            # Precision/positive predictive value
            self.PPV = self.TP / tp_fp_sum
            self.PPV[np.isnan(self.PPV)] = 0
            # Negative predictive value
            self.NPV = self.TN / tn_fn_sum
            self.NPV[np.isnan(self.NPV)] = 0
            # Fall out or false positive rate
            self.FPR = self.FP / tn_fp_sum
            self.FPR[np.isnan(self.FPR)] = 0
            # False negative rate
            self.FNR = self.FN / tp_fn_sum
            self.FNR[np.isnan(self.FNR)] = 0
            # False discovery rate
            self.FDR = self.FP / tp_fp_sum
            self.FDR[np.isnan(self.FDR)] = 0
            # False omission rate
            self.FOR = self.FN / tn_fn_sum
            self.FOR[np.isnan(self.FOR)] = 0
            # Prevalence treshold
            self.PT = (self.TPR * (-self.TNR + 1) + self.TNR - 1) / (self.TPR + self.TNR - 1)
            # Threat score / critical succes index (CSI)
            self.TS = self.TP / (self.TP + self.FN + self.FP)
            self.TS[np.isnan(self.TS)] = 0
            # Overall accuracy for each class
            self.ACC = (self.TP + self.TN) / all_sum
            self.ACC[np.isnan(self.ACC)] = 0
            # balanced accuracy
            self.BA = (self.TPR + self.TNR) / 2
            # F1 score
            self.F1 = (2 * self.TP) / (2 * self.TP + self.FP + self.FN)
            self.F1[np.isnan(self.F1)] = 0
            # Fowlkes–Mallows index
            self.FM = np.sqrt(self.PPV * self.TPR)
            # informedness or bookmaker informedness (BM)
            self.BM = self.TPR + self.TNR - 1
            # markedness (MK) or deltaP
            self.MK = self.PPV + self.NPV - 1
            # todo Matthews correlation coefficient (MCC)
            self.subplot_options = {'nrows': 10, 'ncols': 2, 'figsize': (20, 10)}
            self.heatmap_options = {'annot': True, 'cmap': plt.cm.Blues, 'vmin': 0}

        def visualize(self, labels):
            attributes = self.__dict__.keys()
            fig, axes  = plt.subplots(**self.subplot_options)
            for i, att in enumerate(attributes):
                attribute = getattr(self, att)
                if not isinstance(attribute, np.ndarray):
                    continue

                attribute = attribute.reshape((1, len(labels)))
                df = pd.DataFrame(attribute, index=[att], columns=labels)
                xtick = False
                if i > len(attributes) - 3:
                    xtick = True
                if issubclass(attribute.dtype.type, np.integer):
                    sns.heatmap(df, xticklabels=xtick, ax=axes.flat[i], fmt='d', **self.heatmap_options)
                else:
                    sns.heatmap(df, xticklabels=xtick, ax=axes.flat[i], **self.heatmap_options)
            plt.show()
            return fig
    return Stats()


def get_folders_statistics(directory):
    class Stats:
        def __init__(self, info):
            self.info = dict(sorted(info.items(), key=lambda item: item[0]))
            self.nr_of_elements = sum(info.values())
            self.subplot_options = {'figsize': (10, 5)}
            self.xticks_options = {'rotation': 60, 'horizontalalignment': 'right', 'size': 8}
            self.yticks_options = {'size': 8}
            self.rcParams_options = {"axes.labelsize": 10}

        def bar_plot(self, labels_size=10):
            df = pd.DataFrame(self.info, index=[0])
            fig, ax = plt.subplots(**self.subplot_options)
            f = sns.barplot(data=df, ax=ax)
            f.set(xlabel='Classes', ylabel='Images')
            f.set_xticklabels(f.get_xticklabels(), **self.xticks_options)
            yticks = [int(tick) for tick in f.get_yticks()]
            f.set_yticklabels(yticks, **self.yticks_options)
            plt.rcParams.update(self.rcParams_options)
            return fig

    subfolders, counted_pictures = [], []

    for element in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, element)):
            subfolders.append(element)

    for folder in subfolders:
        path = os.path.join(directory, folder)
        nr_of_pictures = len(os.listdir(path))
        counted_pictures.append(nr_of_pictures)

    inf = {key: value for key, value in zip(subfolders, counted_pictures)}
    return Stats(inf)

