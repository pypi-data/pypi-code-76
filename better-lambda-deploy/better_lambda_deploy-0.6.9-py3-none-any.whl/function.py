from abc import ABC, abstractmethod
import sys


class LambdaFunction(ABC):
    def __init__(self):
        pass

    @classmethod
    def get_handler(cls, *args, **kwargs):
        def handler(event, context):
            return cls(*args, **kwargs).run(event, context)

        return handler

    @abstractmethod
    def run(self, event, context):
        raise NotImplementedError


def lambdahandler(func):
    # Creates dynamic handler in caller's module called MyCallingClassHandler
    module = func.__module__
    handler_name = f"{func.__name__}Handler"
    setattr(sys.modules[module], handler_name, func.get_handler())
    func.is_lambda = True
    return func


class QueueFunction(LambdaFunction):
    pass


class ScheduleFunction(LambdaFunction):
    pass


# def queuetrigger(queue):
#     """
#     Used to decorate a LambdaFunction to define an SQS trigger during deployment.
#     """
#     print("In decorator")
#     print(queue.__name__)

#     def decorator(func):
#         print("In nested decorator")
#         print(func)

#         def wrapper(*args, **kwargs):
#             print("In wrapper")
#             print(args)
#             print(kwargs)
#             return func(args[0])

#         return wrapper

#     print("Out of wrapper")
#     return decorator
