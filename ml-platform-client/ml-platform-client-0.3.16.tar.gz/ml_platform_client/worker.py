import json
import threading
import traceback
from multiprocessing import Process
from multiprocessing.connection import Connection
from typing import List

from .config import GlobalConfig, global_config
from .context import request_context
from .logger import log


class Worker(Process):
    def __init__(self, pipes: List[Connection]):
        super(Worker, self).__init__()
        self.pipes = pipes
        self.model_pool = {}
        self.alg_mapping = {}
        self.tasks = []

    def run(self):
        for pipe in self.pipes:
            self.tasks.append(threading.Thread(target=self.task, args=(pipe,)))
        for task in self.tasks:
            task.start()
        for task in self.tasks:
            task.join()

    def task(self, pipe):
        while True:
            try:
                command, data = pipe.recv()
                if command == 'exit':
                    return
                try:
                    result = self._process(command, data)
                except Exception as e:
                    result = False, None
                    log.error('worker process error: {}, {}'.format(command, e))
                    traceback.print_exc()
                pipe.send(result)
            except Exception as e:
                log.error('worker communication error, {}'.format(e))
                traceback.print_exc()

    def _process(self, command, data):
        if command == 'load':
            return self._process_load(data)
        if command == 'unload':
            return self._process_unload(data)
        if command == 'predict':
            return self._process_predict(data)
        if command == 'init_alg':
            return self._process_init_alg(data)
        if command == 'init_config':
            return self._process_init_config(data)
        return False, None

    def _process_init_alg(self, data):
        self.alg_mapping.update(data)

    def _process_init_config(self, data: GlobalConfig):
        global_config.minio_host = data.minio_host
        global_config.minio_access_key = data.minio_access_key
        global_config.minio_secret_key = data.minio_secret_key
        global_config.minio_secure = data.minio_secure
        return True, None

    def _process_load(self, data):
        model_id = data['model_id']
        model_path = data['model_path']
        algorithm = data['algorithm']
        if algorithm not in self.alg_mapping:
            return False, 'algorithm not support'

        try:
            model = self.alg_mapping[algorithm].load(model_id, model_path)
            self.model_pool[model_id] = model
            return True, None
        except Exception as e:
            log.error('load fail', e)
            log.error(traceback.format_exc())
            return False, 'load fail {}'.format(e)

    def _process_unload(self, data):
        try:
            model_id = data['model_id']
            algorithm = data['algorithm']
            self.alg_mapping[algorithm].unload(model_id)
            if model_id in self.model_pool:
                del self.model_pool[model_id]
            return True, None
        except Exception as e:
            log.error('unload fail', e)
            log.error(traceback.format_exc())
            return False, 'unload fail {}'.format(e)

    def _process_predict(self, data):
        model_id = data['model_id']
        features = data['features']
        params = data['params']
        uuid = data['uuid']
        request_context.uuid = uuid
        if model_id not in self.model_pool:
            message = 'model [{}] not loaded'.format(model_id)
            log.warn(message)
            return False, message

        try:
            prediction = self.model_pool[model_id].predict(features, params)
            log.info('[{}]model: {}, features: {}, prediction: {}, params: {}'
                     .format(uuid, model_id,
                             json.dumps(features, ensure_ascii=False),
                             json.dumps(prediction, ensure_ascii=False),
                             json.dumps(prediction, ensure_ascii=False)))

            return True, prediction
        except Exception as e:
            log.error('predict fail', e)
            log.error(traceback.format_exc())
            return False, 'predict fail {}'.format(e)
        finally:
            request_context.uuid = None
