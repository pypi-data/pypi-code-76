from .algorithm_manager import alg_manager
from .api_util import arg_parse_validation, adapt_to_http_response, api_logger
from .base import BaseApi
from .dispatcher import dispatcher
from .setup import *


class TrainApi(BaseApi):
    api_url = '/train'

    @arg_parse_validation(arg_setup=train_arg_setup, validate_setup=train_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        return alg_manager.train(args['algorithm'], args['model_path'], args['data'],
                                 args['parameter'], args['extend'])


class StatusApi(BaseApi):
    api_url = '/status'

    @arg_parse_validation(arg_setup=status_arg_setup, validate_setup=status_validate_setup)
    @adapt_to_http_response
    @api_logger('status')
    def get(self, args):
        return alg_manager.status(args['algorithm'], args['model_id'])


class PredictApi(BaseApi):
    api_url = '/predict'

    @arg_parse_validation(arg_setup=predict_arg_setup, validate_setup=predict_validate_setup)
    @adapt_to_http_response
    @api_logger('predict')
    def post(self, args):
        return dispatcher.dispatch_predict(args['model_id'], args['features'], args['uuid'], args['params'])


class LoadApi(BaseApi):
    api_url = '/load'

    @arg_parse_validation(arg_setup=load_arg_setup, validate_setup=load_validate_setup)
    @adapt_to_http_response
    @api_logger('load')
    def post(self, args):
        return dispatcher.dispatch_load(args['algorithm'], args['model_id'], args['model_path'])


class UnloadApi(BaseApi):
    api_url = '/unload'

    @arg_parse_validation(arg_setup=unload_arg_setup, validate_setup=unload_validate_setup)
    @adapt_to_http_response
    @api_logger('unload')
    def post(self, args):
        return dispatcher.dispatch_unload(args['algorithm'], args['model_id'])


class DeleteApi(BaseApi):
    api_url = '/delete'

    @arg_parse_validation(arg_setup=delete_arg_setup, validate_setup=delete_validate_setup)
    @adapt_to_http_response
    @api_logger('delete')
    def post(self, args):
        return alg_manager.delete(args['algorithm'], args['model_id'])


class MonitorApi(BaseApi):
    api_url = '/monitor'

    @arg_parse_validation()
    @adapt_to_http_response
    def get(self, args):
        return dispatcher.get_load_info()
