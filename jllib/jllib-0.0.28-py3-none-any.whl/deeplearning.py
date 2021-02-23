import sys
from collections import Counter

import pandas as pd
import numpy as np
import random
import os

import jllib.models
import jllib.models.cnn
import jllib.models.encoder
import jllib.models.fcn
import jllib.models.inception
import jllib.models.mcdcnn
import jllib.models.mcnn
import jllib.models.resnet
import jllib.models.mlp
import jllib.models.tlenet
import jllib.models.twiesn
from jllib.plotting import do_cm, plot_history_df, do_cm_reduce_window_slices
from jllib.utils.utils import calculate_metrics


class AutoEvaluator:
    def __init__(self, x_train: np.ndarray, y_train: np.ndarray, x_val: np.ndarray, y_val: np.ndarray,
                 custom_name: str = '',
                 input_shape: tuple = None,
                 nb_classes: int = None,
                 base_output_directory: str = '_jllib_out',
                 verbose: int = 0,
                 enable_window_slicing=False,
                 window_stride=None,
                 window_size=None,
                 seed=42,
                 kcrossvalidation_k=None,
                 disable_normalization_check=False,
                 shuffle_window_slices=True):
        if not isinstance(x_train, np.ndarray):
            raise TypeError("x_train-parameter is of type " + str(type(x_train)) + ". Expected np.ndarray.")

        if not isinstance(y_train, np.ndarray):
            raise TypeError("y_train-parameter is of type " + str(type(y_train)) + ". Expected np.ndarray.")

        if not isinstance(x_val, np.ndarray):
            raise TypeError("x_val-parameter is of type " + str(type(x_val)) + ". Expected np.ndarray.")

        if not isinstance(y_val, np.ndarray):
            raise TypeError("y_val-parameter is of type " + str(type(y_val)) + ". Expected np.ndarray.")

        self.x_train = x_train
        self.y_train = y_train
        self.x_val = x_val
        self.y_val = y_val

        # sanitize parameters
        if np.isnan(x_train).any():
            raise ValueError('Critical: `x_train` contains NaN values!')
        if np.isnan(x_val).any():
            raise ValueError('Critical: `x_val` contains NaN values!')
        if not disable_normalization_check:
            train_max, train_min = np.amax(x_train), np.amin(x_train)
            val_max, val_min = np.amax(x_val), np.amin(x_val)
            if train_max > 1:
                raise ValueError('Critical: `x_train` contains maximum value ' + str(train_max))
            if val_max > 1:
                raise ValueError('Critical: `val_max` contains maximum value ' + str(val_max))
            if train_min < -1:
                raise ValueError('Critical: `train_min` contains minimum value ' + str(train_min))
            if val_min < -1:
                raise ValueError('Critical: `val_min` contains minimum value ' + str(val_min))

        self.shape = None
        self.nb_classes = None

        if enable_window_slicing:
            if window_stride is None:
                raise TypeError('window_stride must not be None if window slicing is used.')

            if window_size is None:
                raise TypeError('window_size must not be None if window slicing is used.')

            self.x_train, self.y_train, self.train_sample_origin = self._create_slices(x_train,
                                                                                       y_train,
                                                                                       window_stride,
                                                                                       window_size,
                                                                                       shuffle=shuffle_window_slices)
            self.x_val, self.y_val, self.val_sample_origin = self._create_slices(x_val,
                                                                                 y_val,
                                                                                 window_stride,
                                                                                 window_size,
                                                                                 shuffle=shuffle_window_slices)

        self.base_output_directory = base_output_directory + ('' if custom_name == '' else '_' + custom_name)

        self.complete_history_df = None

        self.enable_cnn = True
        self.enable_encoder = True
        self.enable_fcn = True
        self.enable_inception = True
        self.enable_mcdcnn = False
        self.enable_mcnn = False
        self.enable_mlp = True
        self.enable_resnet = True
        self.enable_tlenet = False
        self.enable_twiesn = False

        self.enable_window_slicing = enable_window_slicing

        self.verbose = verbose

        self.base_dir_created = False

        self.seed = seed

        if nb_classes is None:
            # infer classes from labels
            self.nb_classes = len(set(y_train.tolist() + y_val.tolist()))
        else:
            self.nb_classes = nb_classes

        if input_shape is None:
            self.input_shape = self.x_train.shape[1:]
        else:
            self.input_shape = input_shape

        if kcrossvalidation_k is not None:
            raise NotImplementedError("kcrossvalidation_k is not implemented yet.")

    @staticmethod
    def _create_slices(data: np.ndarray,
                       labels: np.ndarray,
                       stride: int,
                       slice_size: int,
                       shuffle: bool = True) -> [np.ndarray, np.ndarray]:
        if not data.shape[0] == labels.shape[0]:
            raise TypeError("Error in AutoEvaluator::_create_slices(). Data and Labels differ in size.")

        if not len(data.shape) <= 3:
            raise TypeError("Error in AutoEvaluator::_create_slices(). Dimension not supported.")

        ret_sliced_data, ret_sliced_labels, ret_sample_origin = [], [], []

        # TODO implement majority voting for evaluation

        for sample_id, (array, label) in enumerate(zip(data, labels)):
            array_slices, label_slices, sample_origin = [], [], []

            lost_samples_cnt, added_cnt = 0, 0

            for step_idx in range(0, array.shape[0], stride):
                arr = array[step_idx:step_idx + slice_size]

                if not arr.any():
                    pass  # do not append if slice consists only of zero
                else:
                    array_slices.append(arr)
                    label_slices.append(label)
                    sample_origin.append(sample_id)

            for i in range(len(array_slices)):
                if array_slices[i].shape == array_slices[0].shape:
                    ret_sliced_data.append(array_slices[i])
                    ret_sliced_labels.append(label_slices[i])
                    ret_sample_origin.append(sample_origin[i])
                    added_cnt += 1
                else:
                    lost_samples_cnt += 1

            if not all(s.shape == array_slices[0].shape for s in array_slices):
                print('Warning: `slices` array created in AutoEvaluator::_create_slices() is ragged. '
                      'Check parameters stride, slice_size and shape of array. Lost',
                      lost_samples_cnt, 'samples and created', added_cnt,
                      'new samples. Check your slicing window settings.', file=sys.stderr)

        ret_sliced_data_np = np.array(ret_sliced_data)
        ret_sliced_labels_np = np.array(ret_sliced_labels)
        sample_origin_np = np.array(ret_sample_origin)

        print('Info: Slicing window data consumes', round(ret_sliced_data_np.nbytes / 1024 / 1024, 2), 'mb.',
              file=sys.stderr)

        # TODO check that supressing null arrays does not result in a skewed data set

        if shuffle:
            return unison_shuffle_np_arrays_3(ret_sliced_data_np, ret_sliced_labels_np, sample_origin_np)
        else:
            return ret_sliced_data_np, ret_sliced_labels_np, sample_origin_np

    def _construct_all_models(self) -> list:
        if not isinstance(self.input_shape, tuple):
            raise TypeError("input_shape-parameter is of type " + str(type(self.input_shape)) + ". Expected tuple.")

        if not isinstance(self.nb_classes, int):
            raise TypeError("input_shape-parameter is of type " + str(type(self.input_shape)) + ". Expected int.")

        if not isinstance(self.base_output_directory, str):
            raise TypeError(
                "base_output_directory-parameter is of type " + str(type(self.input_shape)) + ". Expected str.")

        if not isinstance(self.verbose, int):
            raise TypeError("verbose-parameter is of type " + str(type(self.input_shape)) + ". Expected int.")

        def create_subdir(nn_name, cnt=0):
            try:
                if not self.base_dir_created:
                    dir_to_create = './' + self.base_output_directory + str(cnt) + nn_name
                else:
                    dir_to_create = './' + self.base_output_directory + nn_name
                os.makedirs(dir_to_create)
                if not self.base_dir_created:
                    self.base_dir_created = True
                    self.base_output_directory = self.base_output_directory + str(cnt) + '/'
            except FileExistsError:
                create_subdir(nn_name, cnt + 1)

        def write_summary(model):
            with open(model.output_directory + '/model-summary.txt', 'w') as f:
                from contextlib import redirect_stdout
                with redirect_stdout(f):
                    model.model.summary()

        subdir_lst, models_lst = [], []

        if self.enable_cnn:
            subdir_lst.append('/cnn/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.cnn.Classifier_CNN(self.base_output_directory + subdir_lst[-1],
                                                self.input_shape,
                                                self.nb_classes,
                                                verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_encoder:
            subdir_lst.append('/encoder/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.encoder.Classifier_ENCODER(self.base_output_directory + subdir_lst[-1],
                                                        self.input_shape,
                                                        self.nb_classes,
                                                        verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_fcn:
            subdir_lst.append('/fcn/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.fcn.Classifier_FCN(self.base_output_directory + subdir_lst[-1],
                                                self.input_shape,
                                                self.nb_classes,
                                                verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_inception:
            subdir_lst.append('/inception/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.inception.Classifier_INCEPTION(self.base_output_directory + subdir_lst[-1],
                                                            self.input_shape,
                                                            self.nb_classes,
                                                            verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_mcdcnn:
            subdir_lst.append('/mcdcnn/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.mcdcnn.Classifier_MCDCNN(self.base_output_directory + subdir_lst[-1],
                                                      self.input_shape,
                                                      self.nb_classes,
                                                      verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_mcnn:
            subdir_lst.append('/mcnn/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.mcnn.Classifier_MCNN(self.base_output_directory + subdir_lst[-1],
                                                  self.input_shape,
                                                  self.nb_classes,
                                                  verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_mlp:
            subdir_lst.append('/mlp/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.mlp.Classifier_MLP(self.base_output_directory + subdir_lst[-1],
                                                self.input_shape,
                                                self.nb_classes,
                                                verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_resnet:
            subdir_lst.append('/resnet/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.resnet.Classifier_RESNET(self.base_output_directory + subdir_lst[-1],
                                                      self.input_shape,
                                                      self.nb_classes,
                                                      verbose=self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_tlenet:
            subdir_lst.append('/tlenet/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.tlenet.Classifier_TLENET(self.base_output_directory + subdir_lst[-1], self.verbose)
            write_summary(m)
            models_lst.append(m)

        if self.enable_twiesn:
            subdir_lst.append('/twiesn/')
            create_subdir(subdir_lst[-1])
            m = jllib.models.twiesn.Classifier_TWIESN(self.base_output_directory + subdir_lst[-1], self.verbose)
            write_summary(m)
            models_lst.append(m)

        return models_lst

    @staticmethod
    def enable_gpu_growth():
        return enable_gpu_growth()

    @staticmethod
    def force_cpu_training():
        return force_cpu_training()

    def evaluate(self):
        from tqdm import tqdm

        all_models = self._construct_all_models()

        # fit models and plot training process
        for model in tqdm(all_models):
            self.set_seed()
            model.fit(self.x_train, self.y_train, self.x_val, self.y_val, np.argmax(self.y_val, axis=1))
            self.set_seed()
            self._plot_history(model.output_directory + '/history.csv', type(model).__name__)
            self.set_seed()

        predictions = []

        # perform predictions
        for model in all_models:
            self.set_seed()
            # create a list of metrices
            # Original function has some strange handling of types that's why the parameters are this way.
            if self.enable_window_slicing:
                p = model.predict(self.x_val,
                                  self.y_val,
                                  self.x_train,
                                  np.argmax(self.y_train, axis=1),
                                  np.argmax(self.y_val, axis=1),
                                  return_df_metrics=False)

                p_argmax = np.argmax(p, axis=1)  # prediction
                unique, counts = np.unique(self.val_sample_origin, return_counts=True)
                count_dict = dict(zip(unique, counts))
                gt_argmax = np.argmax(self.y_val, axis=1)  # ground truth

                # iterate over all samples which consist of n slices each
                sample_pred = []
                for sample_origin_id in unique:
                    # find indexes that point at each sample
                    idx_arr = np.where(self.val_sample_origin == sample_origin_id)[0]
                    p_count = p_argmax[idx_arr]
                    cnt = Counter(p_count)
                    cnt.jllib_custom_info = 'In Counter.most_common() the key is the predicted class and the value is ' \
                                            'the amount of votes from window slices.'
                    gt = np.unique(np.argmax(self.y_val[idx_arr], axis=1))
                    assert gt.shape == (1,)
                    sample_pred.append({'pred': cnt.most_common()[0][0],
                                        'counter_obj': cnt,
                                        'ground_truth': gt[0]})

                a_np = np.array([e['pred'] for e in sample_pred])
                b_np = np.array([e['ground_truth'] for e in sample_pred])

                df_metrics = calculate_metrics(a_np, b_np, 0.0)
                self.set_seed()
                predictions.append({type(model).__name__: df_metrics})

                self.set_seed()
                do_cm(self.x_val, self.y_val, model)
                do_cm_reduce_window_slices(a_np, b_np, model.output_directory)
                self.set_seed()
            else:  # no window slicing here
                try:
                    p = model.predict(self.x_val,
                                      self.y_val,
                                      self.x_train,
                                      np.argmax(self.y_train, axis=1),
                                      np.argmax(self.y_val, axis=1))
                except ValueError:
                    # ValueError: Classification metrics can't handle a mix of multilabel-indicator and binary targets
                    p = model.predict(self.x_val,
                                      np.argmax(self.y_val, axis=1),
                                      self.x_train,
                                      np.argmax(self.y_train, axis=1),
                                      np.argmax(self.y_val, axis=1))
                self.set_seed()
                predictions.append({type(model).__name__: p})

                self.set_seed()
                do_cm(self.x_val, self.y_val, model)
                self.set_seed()

        self.complete_history_df.to_csv(self.base_output_directory + '/complete_history.csv')

    def _plot_history(self, path, modelname):
        hist_df = pd.read_csv(path, dtype=np.float)
        hist_df['epoch'] = hist_df.index
        hist_df['modelname'] = modelname

        if self.complete_history_df is None:  # in case of initialization
            self.complete_history_df = hist_df
        else:
            self.complete_history_df = self.complete_history_df.append(hist_df,
                                                                       ignore_index=True,
                                                                       verify_integrity=True)

        plot_history_df(hist_df, path, name=modelname, acc='accuracy')

    def set_seed(self):
        import tensorflow as tf
        tf.keras.backend.clear_session()
        if self.seed is not None:
            tf.random.set_seed(self.seed)
            tf.random.set_seed(self.seed)
            random.seed(self.seed)
            np.random.seed(self.seed)
            os.environ['PYTHONHASHSEED'] = str(self.seed)
            os.environ['TF_CUDNN_DETERMINISTIC'] = '1'

    @staticmethod
    def unison_shuffle_np_arrays(a: np.ndarray, b: np.ndarray):
        return unison_shuffle_np_arrays(a, b)

    @staticmethod
    def create_ohc_labels(labels_array):
        return create_ohc_labels(labels_array)


def unison_shuffle_np_arrays(a: np.ndarray, b: np.ndarray):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def unison_shuffle_np_arrays_3(a: np.ndarray, b: np.ndarray, c: np.ndarray):
    assert len(a) == len(b) == len(c)
    p = np.random.permutation(len(a))
    return a[p], b[p], c[p]


def df_describe_nonscientific(df: pd.DataFrame):
    return df.describe().apply(lambda s: s.apply('{0:.5f}'.format))


def create_ohc_labels(labels_array):
    from sklearn.preprocessing import LabelBinarizer
    lb = LabelBinarizer()
    ret = lb.fit_transform(labels_array)
    return ret


def enable_gpu_growth():
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


def force_cpu_training():
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
