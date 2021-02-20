class MessageError(Exception):
    message = 'Whoops! Something went wrong'

    def __init__(self, message=None, *args, **kwargs):
        self.message = message or self.message
        if args:
            self.message = message.format(*args)
        elif kwargs:
            self.message = message.format(**kwargs)


class ExecutorError(MessageError):
    message = 'An error occurred in the Executor'
