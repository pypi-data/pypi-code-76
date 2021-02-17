class MathError(Exception):
    pass


class MathSyntaxError(MathError):
    def __init__(self, reason="", visualisation=""):
        self.reason = reason
        self.visualisation = visualisation

    def __str__(self):
        return f"Syntax error:\n" \
               f"{self.reason}\n" \
               f"{self.visualisation if self.visualisation else ''}"
