from collections import defaultdict

from flask import Flask
from flask_restful import Api

from .context import request_context
from .logger import log
from .dispatcher import dispatcher
from .api import TrainApi, PredictApi, LoadApi, UnloadApi, MonitorApi, StatusApi, DeleteApi

app = Flask(__name__)
api = Api(app)
api.add_resource(TrainApi, TrainApi.api_url)
api.add_resource(PredictApi, PredictApi.api_url)
api.add_resource(LoadApi, LoadApi.api_url)
api.add_resource(UnloadApi, UnloadApi.api_url)
api.add_resource(MonitorApi, MonitorApi.api_url)
api.add_resource(StatusApi, StatusApi.api_url)
api.add_resource(DeleteApi, DeleteApi.api_url)

preload_models = defaultdict(list)


def set_preload_models(alg, models):
    preload_models[alg].extend(models)


def run_app(port, debug=False):
    global app
    app.run(port=port, debug=debug)


@app.before_first_request
def load_preload_models():
    for alg in preload_models:
        for model_id in preload_models[alg]:
            dispatcher.dispatch_load(alg, model_id, None)


@app.errorhandler(Exception)
def global_handler(e):
    log.error('unhandled exception', e)
    return {'status': 'fail', 'message': str(e)}, 200


@app.teardown_request
def teardown(exception):
    request_context.uuid = None
