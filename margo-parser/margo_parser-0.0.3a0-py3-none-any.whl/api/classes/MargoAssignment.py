from .MargoStatement import MargoStatement 

class MargoAssignment(MargoStatement):

    def __init__(self, name: str, value):

        super().__init__("DECLARATION", name, value=value)

    @property
    def type(self) -> str:
        return "DECLARATION"
