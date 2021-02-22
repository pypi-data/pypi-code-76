import os
import operator
from typing import Optional, TypedDict
from flask import current_app, g, request
from werkzeug.exceptions import Unauthorized
from strawberry.flask.views import GraphQLView
from strawberry.extensions import ExecutionContext, Extension


class UserPayload(TypedDict):
    id: int
    username: str
    email: str


class MyContext(TypedDict):
    current_user: Optional[UserPayload]


class MyGraphQLView(GraphQLView):
    def get_context(self) -> MyContext:
        payload: Optional[UserPayload] = g.current_user

        return {'current_user': payload}


class AuthExtension(Extension):
    def on_request_start(self, *, execution_context: ExecutionContext):
        current_user = execution_context.context.get('current_user')

        if (
            current_user  # Valid login credentials provided
            or execution_context.query
            == 'query __ApolloGetServiceDefinition__ { _service { sdl } }'  # Gateway initialization
            or (os.environ.get('FLASK_ENV') == 'development' and request.headers.get('origin')
                == f"http://localhost:{os.environ.get('NODE_PORT')}")  # GraphiQL request
            or current_app.config['TESTING']  # Test environment
        ):
            return
        else:
            raise Unauthorized()


operator_keys = {
    '': operator.eq,
    '>': operator.ge,
    '<': operator.le,
}
