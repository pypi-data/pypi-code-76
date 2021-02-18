
from ..Phase import Phase
from ..util.Optionizable import Optionizable
from .Decorator import Decorator
from ..util.Logger import classLogger

class ExportValidator(Decorator):
    phase: Phase

    def filter(self, phase : Phase) -> bool:
        self.logDebug("The phase %s has %s exports"%(phase.name, len(phase.exportData)))
        return len(phase.exportData) > 0

    def after(self, phase : Phase):
        project = phase.project
        missingDataNames = []
        for data in phase.exportData:
            if(not project.dataExists(data)):
                missingDataNames.append(data.name)

        if len(missingDataNames) > 0 :
            self.logWarning("The phase %s did not export: %s"%(phase.name, missingDataNames))

