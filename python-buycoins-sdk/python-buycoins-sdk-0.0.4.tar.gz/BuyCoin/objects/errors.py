class Error(BaseException):
    @property
    def response(self):
        return {"message": self.message, "status_code": self.status}


class QueryError(Error):
    def __init__(self, message=None, status=None):
        self.message = message if message else "Invalid Query"
        self.status = status if status else 400


class ClientError(Error):
    def __init__(self, message=None, status=None):
        self.message = message if message else "Unauthorised User"
        self.status = status if status else 401


class InvalidInstance(Error):
    '''
    InvalidInstance class
    '''
    message = 'Not a valid instance of type : '
    manager = ''

    def __init__(self, manager):
        self.manager = manager

    def __str__(self):
        return '%s %s' % (self.message, self.manager)


class ParameterNotAllowed(Error):
    def __init__(self, message=None, status=None):
        self.message = message if message else "Invalid Parameter"
        self.status = status if status else 404
