import json
from functools import wraps

from flask import request, make_response, jsonify, current_app
from flaskerk import HTTPException
from pydantic import ValidationError, BaseModel
from werkzeug import Response

from easi_py_common.core.core import is_iterable_of_models, make_json_response
from easi_py_common.core.error import InvalidIterableOfModelsException


def validate(self, query=None, data=None, resp=None, x=[], tags=[],
             exclude_none: bool = False, response_by_alias: bool = False):
    def decorate_validate_request(func):
        @wraps(func)
        def validate_request(*args, **kwargs):
            json_query, json_data, err = None, None, {}
            # validate query
            arg = request.args
            if not arg:
                arg = {}
            try:
                json_query = query(**arg) if query else None
            except ValidationError as ve:
                err["query"] = ve.errors()
                current_app.logger.error('url：{} validation error: {}'.format(
                    request.url, json.dumps(err)))
            # validate data

            try:
                json_obj = request.get_json()
                if json_obj is None:
                    json_obj = {}
                if isinstance(json_obj, list):
                    json_data = [data(**j) for j in json_obj]
                else:
                    json_data = data(**json_obj) if data else None
            except ValidationError as ve:
                err["data"] = ve.errors()
                current_app.logger.error('url：{} body validation error: {}'.format(
                    request.url, json.dumps(err)))

            if err:
                return make_response(jsonify({'code': 100, 'message': "validation error",
                                              "validation_error": err}), 200)

            request.query = json_query
            request.json_data = json_data

            res = func(*args, **kwargs)

            if isinstance(res, list) or isinstance(res, tuple):
                if is_iterable_of_models(res):
                    return make_json_response(
                        res,
                        200,
                        by_alias=response_by_alias,
                        exclude_none=exclude_none,
                        many=True,
                    )
                else:
                    raise InvalidIterableOfModelsException(res)

            if isinstance(res, BaseModel):
                return make_json_response(
                    res,
                    200,
                    exclude_none=exclude_none,
                    by_alias=response_by_alias,
                )

            if isinstance(res, Response):
                return res
            others = ()
            if isinstance(res, tuple) and len(res) > 1:
                response, others = res[0], res[1:]
            # if resp and not isinstance(response, resp):
            #     abort_json(500, 'Wrong response type produced by server.')

            if resp:
                return make_response(jsonify(**resp.dict()), *others)

            return make_response(resp, *others)

        # register schemas to this function
        for schema, name in zip(
                (query, data, resp), ('query', 'data', 'resp')
        ):
            if schema:
                # assert issubclass(schema, BaseModel)
                self.models[schema.__name__] = schema.schema()
                setattr(validate_request, name, schema.__name__)

        # store exception for doc
        code_msg = {}
        for e in x:
            assert isinstance(e, HTTPException)
            code_msg[str(e.code)] = e.msg

        if code_msg:
            validate_request.x = code_msg

        if tags:
            assert ''.join(tags), 'each tag should be string'
            validate_request.tags = tags

        # register this decorator
        validate_request._decorator = self

        return validate_request

    return decorate_validate_request
