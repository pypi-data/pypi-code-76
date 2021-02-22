class PredicateError(Exception):

    def __init__(self, message: str):
        super(PredicateError, self).__init__()
        self.message = message

    def __repr__(self):
        return f'{self.message}'

    def __str__(self):
        return f'{self.message}'
