import pytest

from simio import AppConfig
from simio.handler.entities import AppRoute
from simio.handler.routes import _create_handler_request
from simio.swagger.fabric import swagger_fabric
from tests.application import (
    sample_handler_post,
    sample_handler_get,
    sample_handler_two_get,
    sample_handler_three_get,
)


@pytest.mark.parametrize(
    "app_config, app_routes, expected_json",
    (
        # fmt: off
        (
            {AppConfig.version: "1.0", AppConfig.name: "test"},
            [
                AppRoute(
                    handler=sample_handler_post,
                    method="post",
                    name="test_handler_one",
                    path="/v1/hello/{user_id}/",
                ),
                AppRoute(
                    handler=sample_handler_get,
                    method="get",
                    name="test_handler_one_get",
                    path="/v1/hello/{user_id}/",
                ),
                AppRoute(
                    handler=sample_handler_two_get,
                    method="get",
                    name="test_handler_two",
                    path="/v1/test/12",
                ),
                AppRoute(
                    handler=sample_handler_three_get,
                    method="get",
                    name="test_handler_three",
                    path="/v1/test/another",
                ),
            ],
            {
                "swagger": "2.0",
                "info": {
                    "version": "1.0",
                    "title": "test"
                },
                "paths": {
                    "/v1/hello/{user_id}/": {
                        "post": {
                            "tags": [
                                "test_handler_one"
                            ],
                            "parameters": [
                                {
                                    "in": "body",
                                    "name": "data",
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "arg_one": {
                                                "type": "string"
                                            },
                                            "arg_two": {
                                                "type": "integer"
                                            },
                                            "arg_three": {
                                                "type": "boolean"
                                            }
                                        }
                                    }
                                },
                                {
                                    'in': 'query',
                                    'name': 'query',
                                    'type': 'integer'
                                },
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "type": "integer"
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            }
                        },
                        "get": {
                            "tags": [
                                "test_handler_one_get"
                            ],
                            "parameters": [
                                {
                                    "in": "query",
                                    "name": "q",
                                    "type": "string"
                                },
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "type": "integer"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            }
                        }
                    },
                    "/v1/test/12": {
                        "get": {
                            "tags": [
                                "test_handler_two"
                            ],
                            "parameters": [
                                {
                                    "in": "query",
                                    "name": "q",
                                    "type": "string"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            }
                        }
                    },
                    "/v1/test/another": {
                        "get": {
                            "tags": [
                                "test_handler_three"
                            ],
                            "parameters": [
                                {
                                    "in": "body",
                                    "name": "some_schema",
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "arg_one": {
                                                "type": "object",
                                                "properties": {
                                                    "key": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "sub_key": {
                                                                    "type": "integer"
                                                                },
                                                                "sub_key2": {
                                                                    "type": "string"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "arg_two": {
                                                "type": "array",
                                                "items": {
                                                    "type": "integer"
                                                }
                                            },
                                            "arg_three": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "integer"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            }
                        }
                    }
                }
            }
        ),
        # fmt: on
    ),
)
def test_swagger_fabric(app_config, app_routes, expected_json):
    for app_route in app_routes:
        handler_request = _create_handler_request(
            app_route.handler, app_route.method, app_route.path
        )
        app_route.handler_request = handler_request

    swagger = swagger_fabric(app_config, app_routes)
    assert swagger.json() == expected_json
