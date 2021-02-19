import abc 

class BaseTaskParam(metaclass=abc.ABCMeta):
    """JUST任务参数的基类

    1. 检查和封装参数
    2. 生成HTTP request的参数"""
    @abc.abstractmethod
    def task_flow_param(self):
        pass
