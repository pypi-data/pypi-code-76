import importlib
import logging

from madeira_utils import loggers, utils


class Dispatch(object):
    def __init__(self, debug=False, mode='test', trace_boto3=False):
        self._logger = loggers.get_logger(level=logging.DEBUG if debug else logging.INFO)
        app_config = utils.load_yaml('config.yaml')

        self._logger.debug('Loading deployment module: %s', app_config['app_type'])
        module = importlib.import_module(f"{__package__}.{app_config['app_type']}")
        # noinspection PyUnresolvedReferences
        self._app = module.App(app_config, debug=debug, mode=mode, trace_boto3=trace_boto3)

    def deploy(self):
        return self._app.deploy()

    def remove(self):
        return self._app.remove()
