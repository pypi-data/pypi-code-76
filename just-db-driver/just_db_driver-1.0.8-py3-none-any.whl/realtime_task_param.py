from just.base_task_param import BaseTaskParam


class RealtimeTaskParam(BaseTaskParam):

    def __init__(self, task_name, sql_txt, ys, yjm, ytm, p):
        assert isinstance(task_name, str), "task_name需要设置为string类型"
        assert isinstance(sql_txt, str), "sql_txt需要设置为string类型"
        self.task_name = task_name
        self.sql_txt = sql_txt
        self.resource = self.RealtimeResource(ys, yjm, ytm, p)

    @property
    def task_flow_param(self):
        settings = {
            "taskName": self.task_name,
            "enableCheckpointing": "False",
            "restartAttempts": 3,
            "notifyType": "not_notify",
            "sqlTxt": self.sql_txt,
            "resource": self.resource()
        }
        return settings

    class RealtimeResource:
        def __init__(self, ys, yjm, ytm, p):
            """
            运行资源配置
            :Param: ys slot数量
            :Param: yjm JobManager内存大小
            :Param: ytm TaskManager内存
            :Param: p 并行度
            """
            assert isinstance(ys, int), "ys（Slot数量）需要设置为int类型"
            assert isinstance(yjm, str), "yjm应设置为“xxg”的string类型"
            assert isinstance(ytm, str), "ytm应设置为“xxg”的string类型"
            assert isinstance(p, int), "p（并行度）应设置为int类型"
            self.ys = ys
            self.yjm = yjm
            self.ytm = ytm
            self.p = p

        def __call__(self):
            rescource_dict = {
                "ys": self.ys,
                "yjm": self.yjm,
                "ytm": self.ytm,
                "p": self.p
            }
            return rescource_dict
