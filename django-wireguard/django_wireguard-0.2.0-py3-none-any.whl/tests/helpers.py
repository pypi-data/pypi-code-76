from typing import List

from django.dispatch import receiver


class SignalHelper:
    def __init__(self, signal_class, sender=None):
        self.signal_class = signal_class
        self.expected_sender = sender
        self.signal_sent = False
        self.signal_sender = None
        self.signal_args = ()
        self.signal_kwargs = {}

    def _handler(self, sender, *args, **kwargs):
        self.signal_sent = True
        self.signal_sender = sender
        self.signal_args = args
        self.signal_kwargs = kwargs

    def __enter__(self):
        self.signal_class.connect(self._handler, sender=self.expected_sender)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.signal_class.disconnect(self._handler, sender=self.expected_sender)
