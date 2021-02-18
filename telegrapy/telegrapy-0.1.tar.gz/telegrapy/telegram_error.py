class InvalidTokenException(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f'"{self.token}" is an invalid token. Check again with @BotFather.'


class ParseException(Exception):
    def __init__(self, to_parse):
        self.to_parse = to_parse

    def __str__(self):
        return f'Unable to parse {self.to_parse}.'