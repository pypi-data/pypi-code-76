import os
from pyPhases import Project
from pyPhases.util.Optionizable import Optionizable
from pyPhases.Data import Data


class Stage(Optionizable):
    name = ""

    def __init__(self, name, options={}):
        self.name = name
        super().__init__(options=options)

    def initialOptions(self, defaultOptions = None):
        return {
            "autorun": True
        }
