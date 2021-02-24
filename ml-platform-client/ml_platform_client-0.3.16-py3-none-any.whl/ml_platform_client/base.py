from flask import request
from flask_restful import Resource
from .validation.validator import ValidatorBase


class BaseApi(Resource):
    api_base_url = '/'

    def options(self):
        return self.get_response({}, 200)

    @staticmethod
    def check_cors(rsp):
        if 'HTTP_ORIGIN' in request.environ.keys():
            rsp.headers["Access-Control-Allow-Origin"] = request.environ['HTTP_ORIGIN']
            rsp.headers["Access-Control-Allow-Methods"] = "*"
            rsp.headers["Access-Control-Max-Age"] = "86400"
            rsp.headers["Access-Control-Allow-Headers"] = "Authorization,Origin,Content-Type,Accept"
        return rsp

    @staticmethod
    def validate(args, setup):
        for key, validator in setup.items():
            if isinstance(validator, list):
                for v in validator:
                    v.set_para_name(key)
                    v.validate(args[key])
            elif isinstance(validator, ValidatorBase):
                validator.set_para_name(key)
                validator.validate(args[key])
