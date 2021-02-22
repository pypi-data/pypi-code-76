class ArgumentException(Exception):
    message = 'Error: invalid arguments'

class InvalidKeyException(Exception):
    message = 'Invalid API key. Contact your account admin to generate a new one, or see our API docs'
    status_code = 401

class NotEnabledException(Exception):
    message = "Your New Relic API access isn't enabled. Contact your account admin, or see our API docs."
    status_code = 403

class ServerErrorException(Exception):
    message = "Something went wrong"
    status_code = 500