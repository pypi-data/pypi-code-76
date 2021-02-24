import inspect
import traceback
from functools import wraps

from flask import Response, request, jsonify
from pymarshaler import Marshal
from pymarshaler.errors import PymarshalError

from pywrapper.errors import StandardError
from pywrapper.handler import get_handler

__MARSHAL = Marshal(ignore_unknown_fields=True)


def json_endpoint(function):
    """
    Auto detect the function argument type and cast the incoming request json as that class type

    Example:

    class Person:
        def __init__(self, name: str): # typing information is necessary
            self.name = name

    @app.route('/print-person', methods=['POST'])
    @json_endpoint
    def print_person(person: Person): # Incoming JSON automatically converted
        print(person)
        return "Printed person correctly!" # Auto transform return value to Http Response object


    :param function: The function accepting/responding with json
    :return: The result of the function as an Http Response object. If no return value is specified returns a
    response with a 200 status code. If the resulting value is a Response object, return the Response directly
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            params = __FunctionParams(function)
            if params.has_json_body():
                json = request.get_json()
                if not json:
                    return Response('JSON body cannot be null input stream', 400)
                result = function(__MARSHAL.unmarshal(params.cls, json), *args, **kwargs)
            else:
                result = function(*args, **kwargs)
            if result:
                return result if isinstance(result, Response) or issubclass(type(result), Response) \
                    else Response(__MARSHAL.marshal(result), 200)
            return jsonify(success=True)
        except Exception as e:
            return __get_error_response(e)
    return wrapper


def __get_error_response(e: Exception) -> Response:
    error_filter = get_handler(type(e))

    if error_filter:
        return error_filter.resolve(e)

    if isinstance(e, StandardError):
        return Response(
            str(e),
            e.code
        )
    elif isinstance(e, PymarshalError):
        return Response(
            str(e),
            400
        )
    else:
        traceback.print_exc()
        return Response(
            "Internal server error.",
            500
        )


class __FunctionParams:
    def __init__(self, function):
        signature = inspect.signature(function).parameters

        if len(signature) != 0:
            self.cls = next(iter((signature.values()))).annotation
        else:
            self.cls = None

    def has_json_body(self):
        return self.cls is not None
