from typing import List, Type, Union

import trafaret as t
from aiohttp.web_exceptions import HTTPBadRequest
from more_itertools import first

from simio.app.config_names import AppConfig
from simio.exceptions import UnsupportedSwaggerType
from simio.swagger.entities import (
    SwaggerConfig,
    SwaggerInfo,
    SwaggerPath,
    SwaggerMethod,
    SwaggerResponse,
    SwaggerProperty,
    SwaggerParameter,
)
from simio.swagger.type_mapping import PYTHON_TYPE_TO_SWAGGER
from simio.handler.entities import HandlerRequest, RequestSchema, AppRoute
from simio.utils import is_typing


def swagger_fabric(app_config: dict, app_routes: List[AppRoute]) -> SwaggerConfig:
    """
        Function to generate swagger config for application

    :param app_config: config[APP]
    :param app_routes: App routes
    :return: SwaggerConfig object
    """
    swagger = SwaggerConfig(
        info=SwaggerInfo(
            version=app_config[AppConfig.version], title=app_config[AppConfig.name],
        ),
    )

    for route in app_routes:
        path = SwaggerPath(path=route.path,)

        if route.handler_request is None:
            continue

        method = _create_swagger_method(route.handler_request, route)
        path.methods.append(method)

        swagger.paths.append(path)

    return swagger


def _create_swagger_method(
    handler_method: HandlerRequest, route: AppRoute
) -> SwaggerMethod:
    method = SwaggerMethod(
        tags=[route.name],
        method=handler_method.method,
        responses=[
            SwaggerResponse(code=200, description="Successful request"),
            SwaggerResponse(
                code=HTTPBadRequest.status_code, description="Invalid input"
            ),
        ],
    )

    if handler_method.request_schema is not None:
        schema_name = handler_method.request_schema.name
        schema = _create_swagger_schema(handler_method.request_schema)
        method.parameters.append(
            SwaggerParameter(in_="body", name=schema_name, schema=schema,)
        )

    for query_arg_name, url_arg_type in handler_method.query_args.items():
        method.parameters.append(
            SwaggerParameter(
                in_="query",
                name=query_arg_name,
                type=_cast_to_swagger_type(url_arg_type),
            )
        )

    for path_arg_name, path_arg_type in handler_method.path_args.items():
        method.parameters.append(
            SwaggerParameter(
                in_="path",
                name=path_arg_name,
                type=_cast_to_swagger_type(path_arg_type),
                required=True,
            )
        )

    return method


def _cast_to_swagger_type(var_type: Union[Type, t.Trafaret]) -> str:
    if is_typing(var_type):
        var_type = var_type.__args__[0]
    elif isinstance(var_type, t.Trafaret):
        var_type = type(var_type)

    if var_type not in PYTHON_TYPE_TO_SWAGGER:
        raise UnsupportedSwaggerType(
            f"Handler argument with type {var_type} is not supported with swagger"
        )

    return PYTHON_TYPE_TO_SWAGGER[var_type]


def _create_swagger_schema(request_trafaret: Union[t.Trafaret, RequestSchema]):
    items_type = _cast_to_swagger_type(request_trafaret.trafaret)

    if items_type == "array":
        items = first(_create_swagger_properties(request_trafaret.trafaret))
        return SwaggerProperty(type="array", items=items)
    if items_type == "object":
        properties = _create_swagger_properties(request_trafaret.trafaret)
        return SwaggerProperty(type="object", properties=properties)
    return SwaggerProperty(type=items_type)


def _create_swagger_properties(request_trafaret: t.Trafaret) -> List[SwaggerProperty]:
    if isinstance(request_trafaret, t.Dict):
        properties = []
        for key in request_trafaret.keys:
            swagger_property = SwaggerProperty(
                name=key.get_name(), type=_cast_to_swagger_type(key.trafaret)
            )
            property_type = _cast_to_swagger_type(key.trafaret)

            if property_type == "array":
                swagger_property.items = first(_create_swagger_properties(key.trafaret))
            elif property_type == "object":
                swagger_property.properties = _create_swagger_properties(key.trafaret)

            properties.append(swagger_property)
        return properties
    if isinstance(request_trafaret, t.List):
        return [_create_swagger_schema(request_trafaret)]

    raise ValueError(f"Found unexpected trafaret type {repr(request_trafaret)}")
