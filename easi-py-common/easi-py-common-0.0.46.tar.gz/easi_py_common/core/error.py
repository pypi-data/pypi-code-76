import json
import sys
import traceback

from flask import jsonify, make_response, current_app
from functools import wraps
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


class ServiceException(Exception):
    """服务异常
    主要针对于一些逻辑异常，就抛出相关的错误。
    比如当前用户不存在，名称不能为空
    """

    def __init__(self, code=400, msg='', data=None, *args, **kwargs):
        self.code = code
        self.message = msg
        self.data = data
        super(ServiceException, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"{}<code:{}, message:{}>".format(self.__class__.__name__, self.code, self.message)

    def __unicode__(self):
        return u"{}<code:{}, message:{}>".format(self.__class__.__name__, self.code, self.message)


class InvalidParmsException(ServiceException):
    def __init__(self):
        super(InvalidParmsException, self).__init__(code=20000, msg='Invalid parameter')


class DataNotFoundException(ServiceException):

    def __init__(self):
        super(DataNotFoundException, self).__init__(msg='data is not found')


class InvalidTokenException(ServiceException):
    def __init__(self):
        super(InvalidTokenException, self).__init__(code=20001, msg='invalid access token')


class TokenExpiredException(ServiceException):
    def __init__(self):
        super(TokenExpiredException, self).__init__(code=20000, msg='token expired')


class RestClientException(ServiceException):
    def __init__(self, code=400, msg='', *args, **kwargs):
        self.code = code
        self.message = msg
        super(RestClientException, self).__init__(code=code, msg=msg, *args, **kwargs)


def intercept_service_exception(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            return ret
        except ServiceException as e:
            if e.data:
                return jsonify(code=e.code, message=e.message, data=e.data)
            return jsonify(code=e.code, message=e.message)

        except ValidationError as v:

            try:
                traceback_exception_list = traceback.format_exception(*sys.exc_info())
                if traceback_exception_list and len(traceback_exception_list) >= 3 and traceback_exception_list[-3]:
                    current_app.logger.error('validation error: {}\n{}'.format(
                        json.dumps(v.errors()), traceback_exception_list[-3].split('\n')[0]))
            except Exception:
                pass

            return make_response(jsonify({'code': 100, 'message': 'validation_error',
                                          "validation error": v.errors()}), 200)
        except IntegrityError:
            return jsonify(code=1100, message=u'重复操作，请稍后再试')

    return wrapped


from typing import List


class BaseFlaskPydanticException(Exception):
    """Base exc class for all exception from this library"""

    pass


class InvalidIterableOfModelsException(BaseFlaskPydanticException):
    """This exception is raised if there is a failure during serialization of
    response object with `response_many=True`"""

    pass


class JsonBodyParsingError(BaseFlaskPydanticException):
    """Exception for error occurring during parsing of request body"""

    pass


class ManyModelValidationError(BaseFlaskPydanticException):
    """This exception is raised if there is a failure during validation of many
    models in an iterable"""

    def __init__(self, errors: List[dict], *args):
        self._errors = errors
        super().__init__(*args)

    def errors(self):
        return self._errors
