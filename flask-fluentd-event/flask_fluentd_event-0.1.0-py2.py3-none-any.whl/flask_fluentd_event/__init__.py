"""Top-level package for Flask Fluentd Event."""

__author__ = """Pyunghyuk Yoo"""
__email__ = "yoophi@gmail.com"
__version__ = "0.1.0"

import logging

from six.moves.queue import Empty, Queue

from fluent import sender


class FluentdEvent(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
            # Send events after every request finishes
            app.after_request(self.send_events)

        # Unbounded queue for sent events
        self.queue = Queue()

    def init_app(self, app):
        tag_prefix = app.config.get("FLUENTD_EVENT_TAG_PREFIX", "flask.fluentd_event")
        host = app.config.get("FLUENTD_EVENT_HOST", "localhost")
        port = int(app.config.get("FLUENTD_EVENT_PORT", 24224))
        self._sender = sender.FluentSender(tag_prefix, host=host, port=port)

        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.send_events)
        else:
            app.teardown_request(self.send_events)

    def event(self, tag, event):
        self.queue.put((tag, event))

    def send_events(self, exception):
        """
        Makes a best-effort to send all the events that it pushed during a
        request but capable of missing some
        """
        pumping = True
        while pumping:
            try:
                tag, event = self.queue.get_nowait()
                self._sender.emit(tag, event)
                self.queue.task_done()
            except Empty:
                pumping = False
            except Exception as e:
                # This is bad but it's worse to foul the request because
                # of a logging issue
                logging.exception(e)
                self.queue.task_done()

        return exception
