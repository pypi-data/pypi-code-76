import logging


class LoggerMultiLineLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger):
        # super(LoggerAdapter, self).__init__(logger, {})
        super().__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        lines = msg.splitlines()
        lines = ['[%s] %s' % (self.prefix, e) for e in lines]
        return lines, kwargs
        # return '[%s] %s' % (self.prefix, msg), kwargs

    def log(self, level, msg, *args, **kwargs):
        """
        Delegate a log call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            if isinstance(msg, (list, tuple)):
                pass
            else:
                msg = [msg]
            for line in msg:
                self.logger.log(level, line, *args, **kwargs)


def logger_ensure_logger(logger_instance):
    if isinstance(logger_instance, logging.LoggerAdapter):
        return logger_instance.logger
    if isinstance(logger_instance, logging.Logger):
        return logger_instance
    if isinstance(logger_instance, (str, bytes)):
        return logging.getLogger(logger_instance)
    raise TypeError("unsupported type {}".format(type(logger_instance)))
