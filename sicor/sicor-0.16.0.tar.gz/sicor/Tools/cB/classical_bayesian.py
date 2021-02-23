import h5py
import json
from random import choice, sample
from copy import copy
from time import time
import logging
from tempfile import TemporaryFile
from psutil import virtual_memory
from tqdm import tqdm
from operator import itemgetter
import numpy as np
from numba import jit


def __zeros__(shape, dtype, max_mem_frac=0.3, logger=None):
    logger = logger or logging.getLogger(__name__)

    # noinspection PyShadowingNames
    def in_memory_array(shape, dtype):
        return np.zeros(shape, dtype)

    # noinspection PyShadowingNames
    def out_memory_array(shape, dtype):
        logger.warning("Not enough memory to keep full image -> fall back to memory map.")
        dat = np.memmap(filename=TemporaryFile(mode="w+b"), dtype=dtype, shape=tuple(shape))
        dat[:] = 0.0
        return dat

    to_gb = 1.0 / 1024.0 ** 3
    mem = virtual_memory().total * to_gb
    arr = int(np.prod(np.array(shape, dtype=np.int64)) * np.zeros(1, dtype=dtype).nbytes * to_gb)

    if arr < max_mem_frac * mem:
        try:
            return in_memory_array(shape, dtype)
        except MemoryError:
            return out_memory_array(shape, dtype)
    else:
        logger.info(
            "Try to create array of size %.2fGB on a box with %.2fGB memory -> fall back to memory map." % (
                arr, mem))
        return out_memory_array(shape, dtype)


def get_clf_functions():
    """
    this is just an example on how one could define classification
    functions, this is an argument to the ToClassifier Classes
    """
    return {
        "ratio": lambda d1, d2: save_divide(d1, d2),
        "index": lambda d1, d2: save_divide(d1 - d2, d1 + d2),
        "difference": lambda d1, d2: to_clf(d1) - to_clf(d2),
        "channel": lambda d: to_clf(d),
        "depth": lambda d1, d2, d3: save_divide(to_clf(d1) + to_clf(d2), d3),
        "index_free_diff": lambda d1, d2, d3, d4: save_divide(to_clf(d1) - to_clf(d2), to_clf(d3) - to_clf(d4)),
        "index_free_add": lambda d1, d2, d3, d4: save_divide(to_clf(d1) + to_clf(d2), to_clf(d3) + to_clf(d4)),
    }


def save_divide(d1, d2, mx=100.0):
    """ save division without introducing NaN's
    :param d1:
    :param d2:
    :param mx: absolute maximum allows value from which on the result is chopped
    :return: d1/d2
    """
    dd1 = to_clf(d1)
    dd2 = to_clf(d2)
    dd2[dd2 == 0.0] = 1e-6
    dd1 /= dd2
    dd1 = np.nan_to_num(dd1)
    dd1[dd1 > mx] = mx
    dd1[dd1 < -mx] = -mx
    return dd1


def to_clf(inp):
    """ helper function which sets the type of features and assures numeric values
    :param inp:
    :return: float array without NaN's or INF's
    """
    return np.nan_to_num(np.array(inp, dtype=float))


class _ToClassifierBase(object):
    def __init__(self, logger=None):
        """ internal base class for generation of classifiers, only to use common __call__

        dummy __init__ which sets all basic needed attributes to none,
        need derived classes to implement proper __init__
        :return:
        """

        self.logger = logger or logging.getLogger(__name__)
        self.n_classifiers = None
        self.classifiers_fk = None
        self.classifiers_id = None
        self.clf_functions = None
        self.classifiers_id_full = None

    def adjust_classifier_ids(self, full_bands, band_lists):
        self.classifiers_id = [np.array([band_lists.index(full_bands[ii]) for ii in clf], dtype=int)
                               for clf in self.classifiers_id_full]
        self.logger.info("""Adjusting classifier channel list indices to actual image, convert from:
%s to \n %s. \n This results in a changed classifier index array from:""" % (str(full_bands), str(band_lists)))
        for func, old, new in zip(self.classifiers_fk, self.classifiers_id_full, self.classifiers_id):
            self.logger.info("%s : %s -> %s" % (func, old, new))

    @staticmethod
    def list_np(arr):
        """
        This is fixing a numpy annoyance where scalar arrays and vectors arrays are treated differently,
        namely one can not iterate over a scalar, this function fixes this in that a python list is
        returned for both scalar and vector arrays
        :param arr: numpy array or numpy scalar
        :return: list with values of arr
        """
        try:
            return list(arr)
        except TypeError:  # will fail if arr is numpy scalar array
            return list(arr.reshape(1))

    def __call__(self, data):
        """
        Secret sauce of the Classical Bayesian approach in python, here the input data->([n_samples,n_data_channels])
        are transformed into ret->([n_samples,n_classifiers])
        Iteration is performed over classifiers_fk (name found in clf_functions) and classifiers_id
        (channel selection from data for this function)
        :param data: n_samples x n_data_channels
        :return: res: n_samples x n_classifiers
        """

        # ret = np.zeros((data.shape[0], self.n_classifiers))  # initialize result
        ret = __zeros__(shape=(data.shape[0], self.n_classifiers), dtype=np.float32)  # initialize result
        for ii, (fn, idx_clf) in enumerate(zip(self.classifiers_fk, self.classifiers_id)):
            # note that that input of clf_function[fn] is a generator expression where
            # iteration is performed over the selected classifiers_id's
            ret[:, ii] = self.clf_functions[fn](*(data[:, ii] for ii in self.list_np(idx_clf)))
        return ret


# noinspection PyMissingConstructor
class ToClassifierDef(_ToClassifierBase):
    def __init__(self, classifiers_id, classifiers_fk, clf_functions, id2name=None, logger=None):
        """ Most simple case of a usable ToClassifier instance, everything is fixed

        classifiers_id: list of lists/np.arrays with indices which are inputs for classifier functions
        classifiers_fk: list of names for the functions to be used
        clf_functions: dictionary for key, value pairs of function names as used in classifiers_fk
        """

        self.logger = logger or logging.getLogger(__name__)
        self.n_classifiers = len(classifiers_fk)
        self.clf_functions = clf_functions
        self.classifiers_id_full = classifiers_id
        self.classifiers_id = classifiers_id
        self.classifiers_fk = classifiers_fk
        self.id2name = id2name

        # assert equal length
        assert len(self.classifiers_id) == self.n_classifiers
        assert len(self.classifiers_fk) == self.n_classifiers
        # assert that used functions are in self.clf_functions
        for cl_fk in self.classifiers_fk:
            assert cl_fk in self.clf_functions
        # assert that each value in the dict is a callable
        for name, func in self.clf_functions.items():
            if hasattr(func, "__call__") is False:
                raise ValueError("Each value in clf_functions should be a callable, error for: %s" % name)


def read_classical_bayesian_from_hdf5_file(filename):
    """ loads persistence data for classical Bayesian classifier from hdf5 file

    :param filename:
    :return: dictionary needed data
    """
    with h5py.File(filename, 'r') as h5f:
        kwargs_mk_clf = {name: json.loads(h5f[name][()]) for name in ["classifiers_fk", "classifiers_id"]}
        kwargs_mk_clf["id2name"] = json.loads(h5f["band_names"][()])

        kwargs_cb = {"bns": [h5f[name][()] for name in json.loads(h5f["bns_names"][()])],
                     "hh_full": h5f["hh_full"][()],
                     "hh": {h5f["%s_key" % name][()]: h5f["%s_value" % name][()] for name in
                            json.loads(h5f["hh_names"][()])},
                     "hh_n": {key: value for key, value in zip(h5f["hh_n_keys"][()], h5f["hh_n_values"][()])},
                     "n_bins": json.loads(h5f["n_bins"][()]), "classes": h5f["classes"][()],
                     "n_classes": json.loads(h5f["n_classes"][()]),
                     "bb_full": [h5f[name][()] for name in json.loads(h5f["bb_full_names"][()])]}

        try:
            mask_legend = {int(key): value for key, value in json.loads(h5f["mask_legend"][()]).items()}
            mask_legend.update({value: key for key, value in mask_legend.items()})
        except KeyError:
            mask_legend = None

        try:
            clf_to_col = {int(key): value for key, value in json.loads(h5f["clf_to_col"][()]).items()}
        except KeyError:
            clf_to_col = None

    return {"kwargs_cb": kwargs_cb,
            "kwargs_mk_clf": kwargs_mk_clf,
            "mask_legend": mask_legend,
            "clf_to_col": clf_to_col
            }


def dict_conv(inp):
    keys, values = [], []
    for key, value in inp.items():
        keys.append(key)
        values.append(value)
    keys = np.array(keys)
    values = np.array(values)
    return keys, values


def write_classical_bayesian_to_hdf5_file(clf, filename, class_names, mask_legend, clf_to_col, band_names):
    with h5py.File(filename, 'w') as h5f:
        for name, data in [("class_names", class_names),
                           ("mask_legend", mask_legend),
                           ("classifiers_fk", clf.mk_clf.classifiers_fk),
                           ("classifiers_id", clf.mk_clf.classifiers_id),
                           ("n_bins", clf.n_bins),
                           ("n_classes", clf.n_classes),
                           ("clf_to_col", clf_to_col),
                           ("band_names", band_names),
                           ]:
            h5f.create_dataset(name, data=json.dumps(data))
        h5f.create_dataset("classes", data=clf.classes)

        keys, values = dict_conv(clf.hh_n)
        h5f.create_dataset("hh_n_keys", data=keys)
        h5f.create_dataset("hh_n_values", data=values)

        h5f.create_dataset("hh_full", data=clf.hh_full, compression="lzf")

        bns_names = []
        for ii, bn in enumerate(clf.bns):
            name = "bns_%i" % ii
            bns_names.append(name)
            h5f.create_dataset(name, data=bn)
        h5f.create_dataset("bns_names", data=json.dumps(bns_names))

        bb_full_names = []
        for ii, bn in enumerate(clf.bb_full):
            name = "bb_full_%i" % ii
            bb_full_names.append(name)
            h5f.create_dataset(name, data=bn)
        h5f.create_dataset("bb_full_names", data=json.dumps(bb_full_names))

        names = []
        for key, value in clf.hh.items():
            name = "hh_%i" % key
            names.append(name)
            h5f.create_dataset("%s_key" % name, data=key)
            h5f.create_dataset("%s_value" % name, data=value, compression="lzf")
        h5f.create_dataset("hh_names", data=json.dumps(names))


def __test__(clf, xx, yy, sample_weight=None, norm="right_class"):
    """
    Test quality of classifier clf using xx as data and yy as truth values.
    :param clf: Classifier, needs to implement a predict method
    :param xx:  data, to be classified -> (n_samples,n_data)
    :param yy:  truth data: -> (n_samples,)
    :param sample_weight: -> weights -> (n_samples)
    :param norm: string which defined which norm to use, implemented are:
            "right_class" : only correct classification causes no penalty,
                            norm value is the fraction of correctly classified data
            "class_distance" : penalty is increasing with increasing class distance,
                               norm value is the normalized mean class distance
    :return: if sample weight is None: value between 0 and 1, one is best
    """
    from scipy.stats import pearsonr  # import here to avoid static TLS ImportError

    if norm == "right_class":
        if sample_weight is None:
            return np.sum(clf.predict(xx) == yy) / float(len(yy))  # ratio of correct
        else:
            yy = np.array(clf.predict(xx) == yy, dtype=int)
            yy[yy == 1] = 1
            yy[yy == 0] = -1
            return np.sum(yy * sample_weight)

    elif norm == "class_distance":
        if sample_weight is None:
            return 1.0 - np.sum(np.abs(np.array(clf.predict(xx) - yy, dtype=float))) / float(
                len(yy) * clf.n_classes)
        else:
            return 1.0 - np.sum(sample_weight *
                                np.abs(np.array(clf.predict(xx) - yy, dtype=float))) / float(
                len(yy) * clf.n_classes)

    elif norm == "scatter":
        if sample_weight is None:
            slope, offset, _ = np.polyfit(x=yy, y=clf.predict(xx), deg=1)
        else:
            slope, offset, _ = np.polyfit(x=yy, y=clf.predict(xx), deg=1, w=sample_weight)
        tst = 1.0 - np.abs(1.0 - slope)
        return tst

    elif norm == "pearson":
        if sample_weight is None:
            tst = pearsonr(x=yy, y=clf.predict(xx))[0]
            return tst
        else:
            raise ValueError("Not implemented")
    elif norm == "histogram":
        if sample_weight is None:
            hh, _, _ = np.histogram2d(clf.predict(xx), yy, bins=clf.n_classes_, normed=True)
            # tst = np.mean(np.diagonal(hh)/(0.5*(np.sum(hh,axis=0)+np.sum(hh,axis=1))))

            tst = 1.0 - np.sum(
                (1.0 - np.diagonal(hh) / (0.5 * (np.sum(hh, axis=0) + np.sum(hh, axis=1)))) ** 2) / clf.n_classes_

            return tst
        else:
            raise ValueError("Not implemented")

    else:
        raise ValueError("Norm %s not implemented." % norm)


def histogramdd_fast(data, bins):
    n_smpl = data.shape[0]
    n_clf = len(bins)
    n_bins = len(bins[0])

    assigns = np.zeros(n_smpl, dtype=int)
    for ii, bb in enumerate(bins):
        assigns += digitize(data[:, ii], bb[1:-1]) * n_bins ** ii

    bc = np.bincount(assigns, minlength=n_bins ** n_clf).reshape(n_clf * [n_bins]).T
    return np.array(bc, dtype=float) / n_smpl


class ClassicalBayesian(object):
    def __init__(self, mk_clf, bns, hh_full, hh, hh_n, n_bins, classes, n_classes, bb_full, logger=None):
        """

        :param mk_clf:
        :param bns:
        :param hh_full:
        :param hh:
        :param hh_n:
        :param n_bins:
        :param classes:
        :param n_classes:
        :param bb_full:
        :return:
        """
        self.logger = logger or logging.getLogger(__name__)
        self.mk_clf = mk_clf
        self.bns = bns
        self.hh_full = hh_full
        self.hh = hh
        self.hh_n = hh_n
        self.n_bins = n_bins
        self.classes = classes
        self.n_classes = n_classes
        self.bb_full = bb_full
        self.zm = 0.5
        self.gs = 0.5
        self.ar_hh_full = {}
        self.ar_hh = {cl: {} for cl in self.classes}

    def __in_bounds__(self, ids):
        ids[ids > self.n_bins - 1] = self.n_bins - 1

    def __predict__(self, xx):
        # import here to avoid static TLS ImportError
        from scipy.ndimage.interpolation import zoom
        from scipy.ndimage.filters import gaussian_filter

        ids = [digitize(ff, bb) - 1 for ff, bb in zip(self.mk_clf(xx).transpose(), self.bb_full)]
        tt = 0
        for ii in ids:
            self.__in_bounds__(ii)
        pp = np.zeros((self.n_classes, len(ids[0])), dtype=float)
        for ii, cl in enumerate(self.classes):
            hh = self.hh[cl][tuple(ids)]
            hh_full = self.hh_full[tuple(ids)]
            hh_valid = hh_full > 0.0
            pp[ii, hh_valid] = hh[hh_valid] / hh_full[hh_valid] / self.n_classes

            hh_invalid = np.logical_not(hh_valid)

            t0 = time()
            if np.sum(hh_invalid) > 0:
                ar_hh_full, ar_hh = None, None
                iw = -1
                while np.sum(hh_invalid) > 0:
                    iw += 1
                    try:
                        ar_hh_full = self.ar_hh_full[iw]
                    except KeyError:
                        if ar_hh_full is None and iw == 0:
                            ar_hh_full = np.copy(self.hh_full)
                        self.ar_hh_full[iw] = gaussian_filter(zoom(ar_hh_full, order=1, zoom=self.zm), sigma=self.gs)
                        ar_hh_full = self.ar_hh_full[iw]
                    try:
                        ar_hh = self.ar_hh[cl][iw]
                    except KeyError:
                        if ar_hh is None and iw == 0:
                            ar_hh = np.copy(self.hh[cl])
                        self.ar_hh[cl][iw] = gaussian_filter(zoom(ar_hh, order=1, zoom=self.zm), self.gs)
                        ar_hh = self.ar_hh[cl][iw]
                    n_bins = ar_hh_full.shape[0]
                    ids_bf = [np.array(id_bf[hh_invalid] * (n_bins / self.n_bins), dtype=int) for id_bf in ids]
                    for ii_bf in ids_bf:
                        ii_bf[ii_bf > n_bins - 1] = n_bins

                    hh_full = ar_hh_full[tuple(ids_bf)]
                    hh = ar_hh[tuple(ids_bf)]
                    good = hh_full != 0.0

                    hh_ok = np.copy(hh_invalid)
                    hh_ok[hh_ok == np.True_] = good  # need element wise comparison here -> use as index field
                    # need element wise comparison here -> use as index field
                    hh_invalid[hh_invalid == np.True_] = np.logical_not(good)
                    pp[ii, hh_ok] = hh[good] / hh_full[good] / self.n_classes
                    self.logger.info("class: %s, bins: %i->%i,curr ok: %i, still bad: %i" %
                                     (str(cl), self.n_bins, n_bins, int(np.sum(hh_ok)), int(np.sum(hh_invalid))))
            tt += time() - t0
        self.logger.info("Time spent in reduced form: %.2f" % tt)
        return pp

    def predict_proba(self, xx):
        pr = self.__predict__(xx.reshape((-1, xx.shape[-1]))).transpose()
        return pr.reshape(list(xx.shape[:-1]) + [pr.shape[-1], ])

    def predict(self, xx):
        pr = self.classes[np.argmax(self.__predict__(xx.reshape((-1, xx.shape[-1]))), axis=0)]
        return pr.reshape(xx.shape[:-1])

    def conf(self, xx):
        proba = self.predict_proba(xx)
        conf = np.nan_to_num(np.max(proba, axis=1) / np.sum(proba, axis=1))
        return conf.reshape(xx.shape[:-1])

    def predict_and_conf(self, xx, bad_data_value=255):
        proba = self.__predict__(xx.reshape((-1, xx.shape[-1]))).transpose()
        pr = self.classes[np.argmax(proba, axis=1)]

        tot = np.sum(proba, axis=1)
        with np.errstate(invalid='ignore'):  # tot might contain zeros -> fix later, is faster that way
            conf = np.max(proba, axis=1) / tot
        conf[tot == 0.0] = 0.0

        pr[conf == 0.0] = bad_data_value
        return pr.reshape(xx.shape[:-1]), conf.reshape(xx.shape[:-1])


# noinspection PyMissingConstructor
class ClassicalBayesianFit(ClassicalBayesian):
    def __init__(self, mk_clf, smooth_min=0.0, smooth_max=2.0, n_bins_min=5, n_bins_max=20, n_runs=10000, smooth_dd=10,
                 max_mb=100.0, norm="right_class", ff=None, xx=None, yy=None, max_run_time=60,
                 sample_weight=None, use_tqdm=False, sufficient_norm=None, dtype=float,
                 fit_method="random", smooth=None, logger=None):
        """
        ff: function of two variables, combines ff_train,ff_test -> ff which is maximised during fit, default
            function is: lambda ff_train,ff_test: 0.5 * (ff_train + ff_test) - 0.4 * np.abs(ff_train-ff_test)
            which has a penalty term for over fitting
        max_mb: maximum size of a histogram array in MB, if the number of bins or features are leading to higher
                needed space, the number of bins is reduced to satisfy max_mb
        """
        self.logger = logger or logging.getLogger(__name__)
        self.fit_method = fit_method
        self.dtype = dtype

        assert hasattr(mk_clf, "__call__")

        if use_tqdm is False:
            # if tqdm shall not be used, use dummy function
            self.tqdm = lambda x: x
        else:
            self.tqdm = tqdm

        if ff is None:
            self.ff = lambda ff_train, ff_test: 0.5 * (ff_train + ff_test) - 0.4 * np.abs(ff_train - ff_test)
        else:
            assert hasattr(ff, "__call__")  # ff should be a callable
            self.ff = ff

        self.norm = norm
        self.idx = None
        self.mk_clf = mk_clf
        self.params = {"mk_clf": self.mk_clf}

        self.sample_weight = None
        self.n_bins = None
        self.classes = None
        self.n_classes = None
        self.classes_ = None
        self.n_classes_ = None

        self.zm = 0.5
        self.gs = 0.5
        self.ar_hh_full = {}

        if hasattr(mk_clf, "__adjust__") is True:
            self.mk_clf = mk_clf

            self.n_bins_min = n_bins_min
            self.n_bins_max = np.min([
                n_bins_max, int(np.floor((max_mb / (np.zeros(1, dtype=self.dtype).nbytes / 1024. ** 2)) ** (
                    1.0 / self.mk_clf.n_classifiers)))])
            assert self.n_bins_max >= self.n_bins_min

            self.n_runs = n_runs
            self.max_run_time = max_run_time
            self.smooth = None

            self.n_bins = None
            self.smooth_values = list(np.around(
                np.linspace(smooth_min, smooth_max, int(smooth_dd)),
                decimals=int(np.ceil(-1 * np.log10((smooth_max - smooth_min) / smooth_dd)))))

            self.params.update({"smooth_min": smooth_min,
                                "smooth_max": smooth_max,
                                "smooth_dd": smooth_dd,
                                "n_bins_min": self.n_bins_min,
                                "n_bins_max": self.n_bins_max,
                                "n_runs": self.n_runs,
                                "norm": self.norm,
                                })

            self.ff_train = None
            self.ff_test = None
            self.ff_res = None

            if xx is not None and yy is not None:
                if type(smooth) is dict:
                    n_bins = int(self.n_bins_min + np.random.sample() * (self.n_bins_max - self.n_bins_min))
                    self.set(xx=xx, yy=yy, sample_weight=sample_weight, n_bins=n_bins, smooth=smooth)
                else:
                    self.fit(xx=xx, yy=yy, sample_weight=sample_weight, sufficient_norm=sufficient_norm)

    def get_params(self, deep=True):
        # for skit learn, to get parameters
        return self.params

    def set_params(self, **params):
        # for skit learn, to set-up new classifier
        if "mk_clf" in params:
            ss = copy(self)
            ss.__init__(**params)
            return ss
        else:
            for name, value in params.items():
                setattr(self, name, value)
            return self

    def mk_hist(self, xx):
        from scipy.ndimage.filters import gaussian_filter  # import here to avoid static TLS ImportError

        hh = histogramdd_fast(xx, self.bns)
        if self.smooth is not None:
            hh = gaussian_filter(hh, self.smooth)
        return np.array(hh, dtype=self.dtype), self.bns

    @staticmethod
    def bins4histeq(inn, nbins_ou=10, nbins_in=1000):
        """
        returns the bin-edges!! for an equalized histogram
        assumes numpy arrays
        """
        hist, bins = np.histogram(inn.flatten(), nbins_in, normed=True)
        cdf = hist.cumsum()
        cdf = cdf / cdf[-1]
        xxx = np.linspace(0., 1., nbins_ou + 1)
        return np.interp(xxx, np.hstack((np.array([0]), cdf)), bins)

    def set(self, xx, yy, smooth=None, n_bins=5, sample_weight=None):
        from sklearn.model_selection import train_test_split  # import here to avoid static TLS ImportError

        self.sample_weight = sample_weight
        self.n_bins = n_bins
        self.classes = np.unique(yy)
        self.ar_hh = {cl: {} for cl in self.classes}
        self.n_classes = len(self.classes)

        self.classes_ = self.classes
        self.n_classes_ = self.n_classes

        if type(smooth) is dict:
            xx_train, xx_test, yy_train, yy_test = train_test_split(xx, yy, test_size=smooth["test_size"],
                                                                    random_state=42)

            left = smooth["min"]
            right = smooth["max"]
            self.__set__(xx_train, yy_train, smooth=left, sample_weight=sample_weight)
            tst_left = __test__(self, xx_test, yy_test, sample_weight=sample_weight, norm=self.norm)

            self.__set__(xx_train, yy_train, smooth=right, sample_weight=sample_weight)
            tst_right = __test__(self, xx_test, yy_test, sample_weight=sample_weight, norm=self.norm)

            for i_steps in range(smooth["steps"]):
                middle = 0.5 * (left + right)
                self.__set__(xx_train, yy_train, smooth=middle, sample_weight=sample_weight)
                tst_middle = __test__(self, xx_test, yy_test, sample_weight=sample_weight, norm=self.norm)

                if (tst_middle + tst_left) > (tst_middle + tst_right):
                    right = copy(middle)
                    tst_right = copy(tst_middle)
                else:
                    left = copy(middle)
                    tst_left = copy(tst_middle)

            if tst_left > tst_middle:
                self.__set__(xx_train, yy_train, smooth=left, sample_weight=sample_weight)
            if tst_right > tst_middle:
                self.__set__(xx_train, yy_train, smooth=right, sample_weight=sample_weight)

        else:  # scalar or None
            tst = self.__set__(xx, yy, smooth=smooth, sample_weight=sample_weight)
            return tst

    def __set__(self, xx, yy, smooth=None, sample_weight=None, test_sample_size=0.05):
        self.smooth = smooth
        xx_clf = self.mk_clf(xx)

        self.bns = [self.bins4histeq(xx, self.n_bins, nbins_in=1000) for xx in xx_clf.transpose()]

        self.hh_full, self.bb_full = self.mk_hist(xx_clf)
        self.hh = {}
        self.hh_n = {}
        for cl in self.classes:
            self.hh[cl], _ = self.mk_hist(xx_clf[yy == cl, :])
            self.hh_n[cl] = np.sum(yy == cl)

        if test_sample_size is None:
            tst = __test__(self, xx, yy, sample_weight=sample_weight, norm=self.norm)
        else:
            if self.idx is None:
                self.idx = np.random.choice(np.arange(xx.shape[0]), np.int(np.ceil(test_sample_size * xx.shape[0])),
                                            replace=False)

            if sample_weight is None:
                sw = None
            else:
                sw = sample_weight[self.idx]

            tst = __test__(self, xx[self.idx, :], yy[self.idx], sample_weight=sw, norm=self.norm)

        return tst

    def fit(self, xx, yy, sample_weight=None, **kwargs):  # keep xx,yy,sample_weight explicit to comply with sklearn
        if self.fit_method == "random":
            self.fit_random(xx, yy, sample_weight=sample_weight, **kwargs)
        elif self.fit_method == "random_bootstrap":
            self.fit_random_bootstrap(xx, yy, sample_weight=sample_weight, **kwargs)
        elif self.fit_method == "chosen_one":
            self.fit_chosen_one(xx, yy, sample_weight=sample_weight, **kwargs)
        else:
            raise ValueError("Method %s not supported." % self.fit_method)

    def fit_chosen_one(self, xx, yy, sample_weight=None, test_size=None, sufficient_norm=None):

        fraction = choice([0.25, 0.5, 0.75])

        n_classifiers_final = self.mk_clf.n_classifiers
        max_run_time = self.max_run_time

        self.n_runs = int(fraction * self.n_runs)
        self.max_run_time = fraction * max_run_time

        self.mk_clf.n_classifiers = 1
        self.mk_clf.n_constant_classifiers = 0
        opts_full = self.fit_random(xx, yy, sample_weight=sample_weight, test_size=test_size,
                                    sufficient_norm=sufficient_norm, return_opts=True)
        opts = []
        for opt in opts_full:
            if opt["ff"] not in [oo["ff"] for oo in opts]:
                opts.append(opt)

        nn = np.max([int(len(opts) / 10), 1])

        choose_from = {"classifiers_id": [oo["classifiers_id"][0] for oo in opts[:nn]],
                       "classifiers_fk": [oo["classifiers_fk"][0] for oo in opts[:nn]],
                       "ff": [oo["ff"] for oo in opts[:nn]]}
        self.mk_clf.choose_from = choose_from
        print("Sample", nn, "Fraction:", fraction)
        print(self.mk_clf.choose_from)

        self.n_runs = int((1 - fraction) * self.n_runs)
        self.max_run_time = (1 - fraction) * max_run_time
        self.mk_clf.n_classifiers = n_classifiers_final
        self.fit_random(xx, yy, sample_weight=sample_weight, test_size=test_size,
                        sufficient_norm=sufficient_norm, return_opts=True)
        self.max_run_time = max_run_time

    def fit_random_bootstrap(self, xx, yy, sample_weight=None, test_size=None, sufficient_norm=None):

        n_classifiers_final = self.mk_clf.n_classifiers
        n_runs_final = self.n_runs
        max_run_time = self.max_run_time

        self.n_runs = int(n_runs_final / n_classifiers_final) + 1
        self.max_run_time = max_run_time / n_classifiers_final

        for ii in range(1, n_classifiers_final + 1):
            if ii == 1:
                self.mk_clf.constant_classifiers = {'classifiers_fk': [], 'classifiers_id': []}
            else:
                self.mk_clf.constant_classifiers = {'classifiers_fk': self.mk_clf.classifiers_fk,
                                                    'classifiers_id': self.mk_clf.classifiers_id}

            # print(self.mk_clf.constant_classifiers)
            self.mk_clf.n_classifiers = ii
            self.mk_clf.n_constant_classifiers = ii - 1
            self.mk_clf.__adjust__()
            self.fit_random(xx, yy, sample_weight=sample_weight, test_size=test_size, sufficient_norm=sufficient_norm)

        # print(self.mk_clf.classifiers_id,self.mk_clf.classifiers_fk)
        self.mk_clf.n_classifiers = n_classifiers_final
        self.n_runs = n_runs_final
        self.max_run_time = max_run_time

    def fit_random(self, xx, yy, sample_weight=None, test_size=None, sufficient_norm=None, return_opts=False):
        from sklearn.model_selection import train_test_split  # import here to avoid static TLS ImportError

        if sample_weight is not None:
            xx_train, xx_test, yy_train, yy_test, sw_train, sw_test = train_test_split(xx, yy, sample_weight,
                                                                                       random_state=42)
        else:
            xx_train, xx_test, yy_train, yy_test = train_test_split(xx, yy, test_size=test_size, random_state=42)
            sw_train, sw_test = None, None
        del sample_weight

        opts = []
        ofx = []
        ofy = []
        t0 = time()
        for ii in self.tqdm(range(self.n_runs)):
            smooth = sample(self.smooth_values, 1)[0]
            n_bins = np.int(self.n_bins_min + np.random.sample() * (self.n_bins_max - self.n_bins_min))
            self.mk_clf.__adjust__()

            ff_train = self.set(xx_train, yy_train, smooth=smooth, n_bins=n_bins, sample_weight=sw_train)
            ff_test = __test__(self, xx_test, yy_test, sample_weight=sw_test, norm=self.norm)
            ff = self.ff(ff_train, ff_test)

            if ff_train > 1.1 * ff_test:
                ofx.append(n_bins)
                ofy.append(smooth)

            opts.append({"ff": np.around(ff, 3), "ii": ii, "smooth": smooth, "ff_test": np.around(ff_test, 3),
                         "ff_train": np.around(ff_train, 3),
                         "n_bins": n_bins, "classifiers_id": self.mk_clf.classifiers_id,
                         "classifiers_fk": self.mk_clf.classifiers_fk})

            if sufficient_norm is not None:
                if ff > sufficient_norm:
                    break
            if (time() - t0) > self.max_run_time:
                break

        opts = sorted(opts, key=itemgetter('ff'), reverse=True)
        opt = opts[0]

        try:
            self.mk_clf.classifiers_id = opt["classifiers_id"]
            self.mk_clf.classifiers_fk = opt["classifiers_fk"]
            self.smooth = opt["smooth"]
            self.n_bins = opt["n_bins"]
            self.set(xx, yy, smooth=opt["smooth"], n_bins=opt["n_bins"])
            self.ff_train, self.ff_test, self.ff_res = opt["ff_train"], opt["ff_test"], opt["ff"]

            if return_opts is True:
                return opts
            else:
                return opt
        except KeyError:
            print("Failed to find a fit for the data")


@jit  # do not use 'nopython=True' here since return arrays are created within this function
def digitize(data, bins, max_bins=2000):
    """
    replacement of np.digitize, speed-up with numba
    """
    bin_map = np.zeros(max_bins, np.int32)
    ret = np.zeros(data.shape[0], dtype=np.int32)

    bin_nn = len(bin_map)
    bin_l = bins[0]
    bin_d = bins[-1] - bins[0]
    bin_dn = bin_d / bin_nn

    bi = 0
    for ii in range(bin_nn):
        if bin_l + ii * bin_dn > bins[bi]:
            bi += 1
        bin_map[ii] = bi

    for ii in range(data.shape[0]):
        bf = int((data[ii] - bin_l) / bin_dn)
        if bf < 1:
            bf = 1
        if bf > max_bins - 1:
            bf = max_bins - 1

        bi = bin_map[bf]

        if data[ii] > bins[bi]:
            bi += 1
        ret[ii] = bi

    return ret
