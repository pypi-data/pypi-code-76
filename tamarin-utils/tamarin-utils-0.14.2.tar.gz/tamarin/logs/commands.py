from tamarin.command import Command
from .models import Report


class ReportCommand(Command):
    def __init__(self, index, status_code, json=None, text=None):
        super(ReportCommand, self).__init__()
        self.index = index
        self.status = status_code
        self.json = json
        self.text = text

    def execute(self):
        try:
            report = Report.objects.create(
                index=self.index,
                status=self.status,
                data=self.json,
                text=self.text,
            )
        except TypeError:
            report = Report.objects.create(
                index=self.index,
                status=self.status,
                text=self.json,
            )
        return {
            'report': report.id
        }
