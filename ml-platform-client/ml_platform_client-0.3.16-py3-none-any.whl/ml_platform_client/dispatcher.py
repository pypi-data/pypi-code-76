import random
import traceback
from collections import defaultdict
from multiprocessing import Pipe
from threading import Lock

from ml_platform_client.logger import log
from .algorithm_manager import alg_manager
from .api_util import catch_exception
from .config import global_config
from .service_response import success_response, success_response_with_data, format_service_response, error_response
from .validation.exceptions import ArgValueError, Warn
from .worker import Worker


class Dispatcher:
    def __init__(self):
        self.num_worker = global_config.num_worker
        self.num_thread = global_config.num_thread
        self.workers = []
        self.pipes = defaultdict(list)
        self.model_load_mapping = defaultdict(list)
        self.status_lock = Lock()
        for i in range(self.num_worker):
            worker_pipes = []
            for _ in range(self.num_thread):
                pipe1, pipe2 = Pipe(True)
                self.pipes[i].append((pipe1, Lock()))
                worker_pipes.append(pipe2)
            worker = Worker(worker_pipes)
            self.workers.append(worker)
            worker.start()

    def get_load_info(self):
        return format_service_response(success_response_with_data({'info': self.model_load_mapping}))

    def register(self, name, alg):
        alg_manager.register(name, alg)
        try:
            for worker in self.pipes:
                pipes = self.pipes[worker]
                for pipe, lock in pipes:
                    with lock:
                        pipe.send(('init_alg', alg_manager.alg_mapping))
                        pipe.recv()
        except Exception as e:
            log.error('register fail')
            log.error(e)

    def set_config(self, config):
        try:
            for worker in self.pipes:
                pipes = self.pipes[worker]
                for pipe, lock in pipes:
                    with lock:
                        pipe.send(('init_config', config))
                        pipe.recv()
        except Exception as e:
            log.error('set config fail')
            log.error(e)

    @catch_exception
    def dispatch_predict(self, model_id, features, uuid, params):
        if model_id not in self.model_load_mapping or len(self.model_load_mapping[model_id]) == 0:
            log.warn('model [{}] not loaded'.format(model_id))
            raise Warn(message='model [{}] not loaded'.format(model_id))

        candidates = self.model_load_mapping[model_id]
        index = random.choice(candidates)
        pipe, lock = random.choice(self.pipes[index])
        try:
            with lock:
                pipe.send(('predict', {'model_id': model_id, 'features': features, 'uuid': uuid, 'params': params}))
                success, predictions = pipe.recv()
                # 如果返回的是模型未加载，重置模型加载状态

            if not success and 'load' in predictions:
                with self.status_lock:
                    self.model_load_mapping[model_id].remove(index)

        except Exception as e:
            log.error(e)
            traceback.print_exc()
            log.error('fail to call worker')
            return format_service_response(error_response(message='worker fail'))

        if success:
            return format_service_response(success_response_with_data({'predictions': predictions}))
        else:
            return format_service_response(error_response(message=str(predictions)))

    @catch_exception
    def dispatch_unload(self, algorithm, model_id):
        if algorithm not in alg_manager.alg_mapping:
            raise ArgValueError(message='algorithm [{}] not support'.format(algorithm))

        if model_id not in self.model_load_mapping:
            return format_service_response(success_response('model is not loaded'))

        with self.status_lock:
            for index in self.model_load_mapping[model_id]:
                for pipe, lock in self.pipes[index]:
                    with lock:
                        pipe.send(('unload', {
                            'algorithm': algorithm,
                            'model_id': model_id
                        }))
                        success, _ = pipe.recv()

            self.model_load_mapping[model_id] = []
        return format_service_response(success_response())

    @catch_exception
    def dispatch_load(self, algorithm, model_id, model_path):
        if algorithm not in alg_manager.alg_mapping:
            raise ArgValueError(message='algorithm [{}] not support'.format(algorithm))

        if model_id in self.model_load_mapping and len(self.model_load_mapping[model_id]) > 0:
            log.info('model is already loaded {}'.format(model_id))
            return format_service_response(success_response('model is already loaded'))
            # raise ArgValueError(message='model [{}] already loaded'.format(model_id))

        index = random.randint(0, self.num_worker - 1)
        pipe, lock = random.choice(self.pipes[index])
        with lock:
            pipe.send(('load', {
                'model_id': model_id,
                'model_path': model_path,
                'algorithm': algorithm
            }))
            success, message = pipe.recv()
        if success:
            with self.status_lock:
                self.model_load_mapping[model_id].append(index)
            return format_service_response(success_response())
        else:
            return format_service_response(error_response(message=message))


dispatcher = Dispatcher()


def register(name, alg):
    global dispatcher
    dispatcher.register(name, alg())


def set_config(config):
    global dispatcher
    dispatcher.set_config(config)
