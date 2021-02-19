from just.base_task_param import BaseTaskParam


class OfflineTaskParam(BaseTaskParam):

    def __init__(self, task_name, db_name, sql_txt, num_executors,
                 driver_cores, executor_cores, driver_memory,
                 executor_memory, conf=None):

        assert isinstance(task_name, str), "task_name需要设置为string类型"
        assert isinstance(db_name, str), "db_name需要设置为string类型"
        assert isinstance(sql_txt, str), "sql_txt需要设置为string类型"
        self.task_name = task_name
        self.db_name = db_name
        self.sql_txt = sql_txt
        self.resource = self.OfflineResources(num_executors, driver_cores,
                                              executor_cores, driver_memory,
                                              executor_memory, conf)

    @property
    def task_flow_param(self):
        settings = {
            "inputNodes": [],
            "paths": [],
            "jobs": [{
                "jobType": "just_sql",
                "jobName": "JUST",
                "coordX": 160,
                "coordY": 160,
                "nodeId": "nodeId",
                "dbName": self.db_name,
                "sqlTxt": self.sql_txt,
                "resource": self.resource()
            }]
        }
        return settings

    @property
    def task_edit_param(self):
        settings = {
            "taskName": self.task_name,
            "failureAction": "finishPossible",
            "notifyType": "not_notify"
        }
        return settings

    class OfflineResources:
        def __init__(self, num_executors, driver_cores,
                     executor_cores, driver_memory, executor_memory, conf):
            assert isinstance(num_executors, int), "num_executors需要设置为int类型"
            assert isinstance(driver_cores, int), "driver_cores需要设置为int类型"
            assert isinstance(executor_cores, int), "executor_cores需要设置为int类型"
            assert isinstance(driver_memory, str), "driver_memory需要设置为string类型"
            assert isinstance(executor_memory, str), \
                "executor_memory需要设置为string类型"
            if conf is not None:
                assert isinstance(conf, dict), "conf需要设置为kv的dict类型"
            self.num_executors = num_executors
            self.driver_cores = driver_cores
            self.driver_memory = driver_memory
            self.executor_memory = executor_memory
            self.conf = conf

        def __call__(self):
            resource_dict = {
                "driverCores": self.driver_cores,
                "numExecutor": self.num_executors,
                "driverMemory": self.driver_memory,
                "executorMemory": self.executor_memory
            }
            if self.conf is not None and len(self.conf) > 0:
                resource_dict["conf"] = self.conf
            return resource_dict
