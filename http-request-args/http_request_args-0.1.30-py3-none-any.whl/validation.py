from flask import request
from flask_restplus import reqparse
from .status import ArgumentsStatus
from .qs_parser import QueryStringParser
from .argument import ListArgument
from functools import wraps
import json

from http_status_code.standard import request_args_validation_error, successful_request

class RequestArgsValidator:
    """ A class responsible for query string and body arguments validation """
    def __init__(self, qs_args_def=list(), body_args_def=list()):
        self.qs_args_def = qs_args_def
        self.body_args_def = body_args_def
        self.qs_args = QueryStringParser.parse_args(self.qs_args_def)
        self.body_args = RequestArgsValidator.get_body_args()
        self.validation_report = {'body': dict(), 'query_string': dict()}
        self.invalid = False

    @staticmethod
    def get_body_args():
        # Body data sent with file
        json_data = request.files.get('data')
        if json_data:
            return json.load(json_data)

        # Body data sent through json
        elif request.json is not None:
            return request.json

        # No Body data
        else:
            return dict()



    def update_validation_report(self, key, msg_ifo):
        self.set_invalid_validation()
        self.validation_report[key].update(msg_ifo)

    def set_invalid_validation(self):
        self.invalid = True

    @staticmethod
    def help(qs_args_def, body_args_def):
        help_report = dict()
        # 1- Check the query string
        if len(qs_args_def):
            qs_status = ArgumentsStatus('query_string', qs_args_def)
            qs_status.args_help()
            help_report.update(qs_status.help_report)

        # 2- Check the body args
        if len(body_args_def):
            body_status = ArgumentsStatus('body', body_args_def)
            body_status.args_help()
            help_report.update(body_status.help_report)

        return help_report

    def validate(self):
        # 1- Check the query string
        #if len(self.qs_args_def):
        qs_status = ArgumentsStatus('query_string', self.qs_args_def)
        qs_status.assert_args(self.qs_args)

        if qs_status.invalid_args:
            self.update_validation_report('query_string', qs_status.validation_report)

        # 2- Check the body args
        #if len(self.body_args_def):
        body_status = ArgumentsStatus('body', self.body_args_def)
        body_status.assert_args(self.body_args)

        if body_status.invalid_args:
            self.update_validation_report('body', body_status.validation_report)

    @staticmethod
    def args_validation(qs_args_def, body_args_def):
        def decorator(fn):
            """A decorator for all of the actions to do try except"""

            @wraps(fn)
            def wrapper(*args, **kwargs):
                if 'help' in request.headers and request.headers['help'] == 'help':
                    return successful_request, RequestArgsValidator.help(qs_args_def, body_args_def)
                
                req_validator = RequestArgsValidator(qs_args_def, body_args_def)
                req_validator.validate()
                
                if req_validator.invalid:
                    request.qs_args = request.args
                    request.body_args = request.json

                    return request_args_validation_error, req_validator.validation_report
                
                else:
                    # Action
                    request.qs_args = req_validator.qs_args
                    request.body_args = req_validator.body_args

                    status, data = fn(*args, **kwargs)
                    return status, data

            return wrapper

        return decorator