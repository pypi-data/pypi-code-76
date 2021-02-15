from copy import copy
from tempfile import NamedTemporaryFile

import numpy as np
import torch
from ignite.engine import Events

from ...helpers import call

# TODO: Update docs to refer to arbitrary engines, not just "train",
# "validation" and "test"
class MetricsAttacher:
    """
    Helper evaluator class for attaching metrics to engines.

    It attaches Ignite metrics to the train, validation and test engines such
    that whenever they finish running the runner logs them.
    """
    def __init__(self, metrics, output_transform=lambda x: x):
        """
        Args:
            metrics (dict of str:ignite.metrics.Metric): metrics to track and
                their tags. Values of the dictionary are uninitialized classes.
            output_transform (function): A function to transform outputs of
                runners into a format parsed by metrics objects. Each metric
                can have its own individual transform which overrides this
                option.
        """
        self._metrics = metrics
        self._output_transform = output_transform

    def attach(self, sacred_run, engine_names, *engines):
        """
        Attach the engines to the logger.
        """
        for name, metric in self._metrics.items():
            for engine in engines:
                metric_obj = call(metric,
                                  default_params={'output_transform': self._output_transform})
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

class EngineOutputTracker:
    """A class that keeps outputs of an ignite engine."""
    def __init__(self, output_transform=lambda x: x):
        self._output_transform = output_transform
        self._outputs = None

    def update_output_from_engine(self, engine):
        self.update_output(engine.state.output)

    def update_output(self, output):
        transformed_output = self._output_transform(output)
        if self._outputs is None:
            self._outputs = transformed_output
            if type(self._outputs) == tuple:
                self._outputs = list(self._outputs)
        else:
            if type(transformed_output) == tuple:
                for i in range(len(transformed_output)):
                    self._outputs[i] = torch.cat(
                        (self._outputs[i], transformed_output[i]))
            else:
                self._outputs = torch.cat(
                    (self._outputs, transformed_output))

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
