
class ValidationBroker(Exception):

    def __init__(self):
        self.message = 'Need a broker to use Arsene'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
