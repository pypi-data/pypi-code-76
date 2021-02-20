from .model import Model

class Cerami(object):
    def __init__(self, client):
        self.client = client

    @property
    def Model(self):
        """return a model with a connected client"""
        model_cls = Model
        model_cls.client = self.client
        return model_cls
