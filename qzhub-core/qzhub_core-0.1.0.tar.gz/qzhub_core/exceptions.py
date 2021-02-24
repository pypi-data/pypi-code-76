class UnderConstructionError(Exception):
    def __init__(self, tag, message="Block of code is under construction"):
        self.tag = tag
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.tag.upper()} -> {self.message}"
