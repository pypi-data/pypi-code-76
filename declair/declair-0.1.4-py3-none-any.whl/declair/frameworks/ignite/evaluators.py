from copy import copy
from tempfile import NamedTemporaryFile

import numpy as np
import torch
from ignite.engine import Events

from ...serialization import string_to_type

def attach_metrics(sacred_run, engines, metrics, output_transform=lambda x: x):
    """
    Helper function for initializing and attaching metrics to multiple engines.
    It takes in a list of engines and a dictionary of <metric name: metric>
    pairs, with a possible output_transform to apply to these metrics.

    The `metrics` parameter is a dictionary which defines metrics to be
    initialized and attached to the engines. The form is quite flexible, but in
    general it's like below:
    {
        'accuracy': 'ignite.metrics.Accuracy',
        'precision': {
            'metric': 'ignite.metrics.Precision',
            'kwargs': {
                'average': True
            }
        }
    }

    Args:
        metrics (dict of str:dict): Dictionary of metrics to track.
            Every key either refers to a Metric type to instantiate, a type
            string to import and instantiate, or a dictionary. If it is a
            dictionary, then it must contain a key `metric` which refers to a
            type or type string, and it may contain an entry `kwargs` which is
            a dictionary or keyword arguments to provide.

        output_transform (function): A function to transform outputs of
            engines into a format parsed by metrics objects. Each metric
            can have its own individual transform which overrides this
            option, defined in its `kwargs` dictionary entry.
    """
    default_kwargs = {
        'output_transform': output_transform
    }
    for name, metric in metrics.items():
        if callable(metric):
            metric_type = metric
            kwargs = default_kwargs
        elif isinstance(metric, str):
            metric_type = string_to_type(metric)
            kwargs = default_kwargs
        elif isinstance(metric, dict):
            if 'metric' in metric:
                m = metric['metric']
                if callable(m):
                    metric_type = m
                elif isinstance(m, str):
                    try:
                        metric_type = string_to_type(m)
                    except:
                        raise ValueError('Could not import Ignite metric type {} for metric {}'.format(
                        m, name))
                else:
                    raise ValueError("'metric' key of metrics must be a type to instantiate or a type string.")
            else:
                raise ValueError("`metrics` dict entries must be dictionaries with a key 'metric' which refers to the metric type to instantiate. {} does not have such a key".format(name))
            if 'kwargs' in metric:
                kwargs = copy(metric['kwargs'])
                if 'output_transform' not in kwargs:
                    kwargs['output_transform'] = output_transform
            else:
                kwargs = default_kwargs
        else:
            raise ValueError("`metrics` dict entries must be types, type strings or dictionaries. {} is neither".format(name))

        for engine in engines:
            metric_obj = metric_type(**kwargs)
            metric_obj.attach(engine, name)

class SacredMetricsLogger:
    """
    Evaluator class for logging values of ignite metrics into the Sacred runner.
    """
    def __init__(self, tracked_metrics={}):
        """
        Args:
            tracked_metrics (dict of str:list of str): Names of metrics from
                each engine, 'train', 'val' and 'test' to track. If any of
                these keys isn't provided, then all of the engine's metrics are
                tracked.
        """
        self._tracked_metrics = tracked_metrics
        self._sacred_run = None
        self._main_engine = None
        self._removable_refs = None

    def _update_metrics_from_engine(self, engine, engine_name):
        # we explicitly refer to self._main_engine instead of engine because
        # it's the engine which defines the current epoch of training
        # (presumably it's the train engine)
        epoch = self._main_engine.state.epoch
        metric_names = self._tracked_metrics.get(engine_name, engine.state.metrics.keys())
        for metric in metric_names:
            key = "{}_{}".format(engine_name, metric)
            value = engine.state.metrics[metric]
            self._sacred_run.log_scalar(key, value, epoch)

    def attach(self, sacred_run, engine_names, *engines):
        """
        Attach the engines to the logger.
        """
        self._sacred_run = sacred_run
        self._main_engine = engines[0]
        self._removable_refs = []
        for name, engine in zip(engine_names, engines):
            ref = engine.add_event_handler(Events.EPOCH_COMPLETED,
                                           self._update_metrics_from_engine,
                                           name)
            self._removable_refs.append(ref)

    def detach(self):
        if self._removable_refs is None:
            return

        for ref in self._removable_refs:
            ref.remove()
        self._removable_refs = None

def _output_of_tensors_to_numpy_matrix(output):
    # this is used if a model returns, for example, a tuple of tensors
    # (y_pred, y) where both of them contain a full batch of values
    # For each sample in the batch we want a row of all predicted values and
    # the desired output; keep in mind that predictions of a model may be a
    # vector of values
    batch_size = output[0].shape[0]
    for v in output:
        if v.shape[0] != batch_size:
            raise ValueError("Output has varying batch sizes")
    maxdim = max(o.dim() for o in output)
    numpified = []
    for o in output:
        o_numpified = o.cpu().detach().numpy()
        while len(o_numpified.shape) < maxdim:
            o_numpified = np.expand_dims(o_numpified, axis=1)
        numpified.append(o_numpified)
    return np.hstack(numpified)

def _detach_if_possible(obj):
    try:
        return obj.cpu().detach()
    except AttributeError:
        return obj

class EngineOutputTracker:
    """A class that keeps outputs of an ignite engine. The outputs are expected
    to be batch tensors, either in a tuple or as a single tensor. This object
    concatenates them into long tensors of all occurring values, as if it was
    one big batch.

    If the engine outputs a tuple, a concatenated tensor is kept for every
    tensor in the tuple.

    If the engine outputs a single object, a single concatenated tensor is
    kept.

    The tensors are detached from the computational graph before being concatenated.
    """
    def __init__(self, output_transform=lambda x: x):
        self._output_transform = output_transform
        self._outputs = None

    def update_output_from_engine(self, engine):
        self.update_output(engine.state.output)

    def update_output(self, output):
        transformed_output = self._output_transform(output)
        if self._outputs is None:
            self._outputs = _detach_if_possible(transformed_output)
            if type(self._outputs) == tuple:
                self._outputs = [_detach_if_possible(o)
                                 for o in self._outputs]
        else:
            if type(transformed_output) == tuple:
                for i in range(len(transformed_output)):
                    self._outputs[i] = torch.cat(
                        (self._outputs[i], _detach_if_possible(transformed_output[i])))
            else:
                self._outputs = torch.cat(
                    (self._outputs, _detach_if_possible(transformed_output)))

    def clear_output(self, engine=None):
        self._outputs = None

    def get_output(self):
        return self._outputs

    def attach_engine(self, engine):
        engine.add_event_handler(Events.EPOCH_STARTED,
                                  self.clear_output)
        engine.add_event_handler(Events.ITERATION_COMPLETED,
                                   self.update_output_from_engine)

class EngineOutputSaver(EngineOutputTracker):
    """Class responsible for tracking and saving outputs of a single Ignite
    engine.
    """
    def __init__(self, output_transform=lambda x: x):
        super().__init__(output_transform)
        self._savefile = None

    def save_output(self):
        if type(self._outputs) == list:
            outputs = _output_of_tensors_to_numpy_matrix(self._outputs)
        else:
            outputs = self._outputs.cpu().detach().numpy()
        if self._savefile is not None:
            self._savefile.close()
        if self._outputs is None:
            raise ValueError("No outputs to save")
        self._savefile = NamedTemporaryFile()
        np.savetxt(self._savefile.name, outputs)
        self._savefile.flush()
        return self._savefile.name

    def clear_output(self, engine=None):
        super().clear_output(engine=engine)
        if self._savefile is not None:
            self._savefile.close()
            self._savefile = None

class SacredOutputSaver:
    def __init__(self, output_saver_transforms={}, clear_on_completion=True):
        self._sacred_run = None
        self._savers = {}
        self._output_saver_transforms = output_saver_transforms
        self._clear_on_completion = clear_on_completion

    def _completed(self, engine, name):
        self._complete[name] = True
        if all(v for v in self._complete.values()):
            for name, saver in self._savers.items():
                filename = saver.save_output()
                self._sacred_run.add_artifact(filename, "{}_outputs".format(name))
                if self._clear_on_completion:
                    saver.clear_output()

    def attach(self, sacred_run, engine_names, *engines):
        """
        Instantiate and attach all metrics to the engines.
        """
        self._sacred_run = sacred_run
        self._complete = {
            name: False for name in engine_names
        }
        for name in engine_names:
            transform = self._output_saver_transforms.get(name, lambda x: x)
            self._savers[name] = EngineOutputSaver(transform)
        for name, engine in zip(engine_names, engines):
            self._savers[name].attach_engine(engine)
            engine.add_event_handler(Events.COMPLETED, self._completed, name)

    def get_savers(self):
        return self._savers
