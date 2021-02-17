from .MargoStatement import MargoStatement 

class MargoDirective(MargoStatement):

    def __init__(self, name: str):
        super().__init__("DIRECTIVE", name)

    @property
    def type(self) -> str:
        return "DIRECTIVE"

    @property
    def value(self) -> any:
        return None