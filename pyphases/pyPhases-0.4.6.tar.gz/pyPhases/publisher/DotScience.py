from ..Phase import Phase
from .Publisher import Publisher

import os
import dotscience

class DotScience(Publisher):
    connected = False

    def publish(self, phase: Phase):
        if (DotScience.connected == False):
            self.log("Connect")
            dotscience.connect(
                self.getOption("username"),
                self.getOption("apikey"),
                self.getOption("projectname"),
                self.getOption("url"),
            )
            dotscience.start()
            DotScience.connected = True

        MODEL_DIR = "./dist/model"

        if (phase.config):
            for (value, name) in enumerate(phase.config):
                value = phase.config[name]
                self.log("add parameter: %s = %s"%(name, str(value)))
                dotscience.parameter(name, value)
        if (phase.metrics):

            for (value, name) in enumerate(phase.metrics):
                value = phase.metrics[name]
                self.log("add metric: %s = %s"%(name, str(value)))
                dotscience.metric(name, value)

        if (phase.summary):
            for (value, name) in enumerate(phase.summary):
                value = phase.summary[name]
                self.log("add summary: %s = %s"%(name, str(value)))
                dotscience.summary(name, value)

        if (phase.inputs):
            for value in enumerate(phase.inputs):
                self.log("add input: %s"%(value, str(value)))
                dotscience.input(value)

        if (phase.model):
            if not os.path.isdir(MODEL_DIR):
                os.makedirs(MODEL_DIR)

            export_path = os.path.join(MODEL_DIR)

            modelName = self.getOption("modelName")
            modelType = self.getOption("modelType")

            phase.model.save(export_path + "/" + modelName)
            self.log("export model")
            dotscience.model(modelType, modelName, MODEL_DIR)
            dotscience.publish("training for " + modelName, deploy=False)
            self.log("publish finished")
