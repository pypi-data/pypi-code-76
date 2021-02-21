

class Report():

    def __init__(self, filename: str):
        self._filename = filename

    @property
    def filename(self):
        return self._filename
