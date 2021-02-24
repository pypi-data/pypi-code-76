import time
from threading import Thread

from .mysql_accessor import MysqlAccessor
from .algorithm_manager import alg_manager
from .dispatcher import dispatcher


class Checker(Thread):

    update_time_mapping = {}

    def run(self):
        while True:
            algs = alg_manager.alg_mapping.keys()
            for algorithm in algs:
                update_time = MysqlAccessor.check_load_update_time(algorithm)
                if not update_time:
                    continue

                if algorithm not in self.update_time_mapping or update_time > self.update_time_mapping[algorithm]:
                    models = MysqlAccessor.get_load_models(algorithm)
                    to_load_models = models.keys()
                    loaded_models = dispatcher.all_loaded_models
                    need_load_models = to_load_models - loaded_models
                    need_unload_models = loaded_models - to_load_models

                    for model_id in need_load_models:
                        dispatcher.dispatch_load(algorithm, model_id, models[model_id])

                    for model_id in need_unload_models:
                        dispatcher.dispatch_unload(algorithm, model_id)

                    self.update_time_mapping[algorithm] = update_time

            time.sleep(5)


checker = Checker()
