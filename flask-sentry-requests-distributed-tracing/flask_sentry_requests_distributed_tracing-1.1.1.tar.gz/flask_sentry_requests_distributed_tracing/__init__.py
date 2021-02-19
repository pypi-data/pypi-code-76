from uuid import uuid4
from functools import wraps
import requests
from flask import request
import sentry_sdk


def flask_sentry_requests_distributed_tracing(app):
    with app.app_context():
        # NOTE: Setting here so it is present in crons/workers running in flask context
        sentry_sdk.set_tag("request-id", str(uuid4()))

        @app.before_request
        def _setup_sentry_scope():
            request_id = str(request.headers.get("x-request-id") or uuid4())
            sentry_sdk.set_tag("request-id", request_id)

        def _header_wrapper(f):
            @wraps(f)
            def wrapper(*args, **kwgs):
                with sentry_sdk.configure_scope() as scope:
                    request_id = scope._tags.get("request-id") or str(uuid4())
                    headers = kwgs.pop("headers", None) or {}
                    headers["x-request-id"] = request_id
                    return f(*args, headers=headers, **kwgs)

            return wrapper

        requests.request = _header_wrapper(requests.request)
        requests.get = _header_wrapper(requests.get)
        requests.options = _header_wrapper(requests.options)
        requests.head = _header_wrapper(requests.head)
        requests.post = _header_wrapper(requests.post)
        requests.put = _header_wrapper(requests.put)
        requests.patch = _header_wrapper(requests.patch)
        requests.delete = _header_wrapper(requests.delete)
        requests.Session.request = _header_wrapper(requests.Session.request)
        requests.Session.get = _header_wrapper(requests.Session.get)
        requests.Session.options = _header_wrapper(requests.Session.options)
        requests.Session.head = _header_wrapper(requests.Session.head)
        requests.Session.post = _header_wrapper(requests.Session.post)
        requests.Session.put = _header_wrapper(requests.Session.put)
        requests.Session.patch = _header_wrapper(requests.Session.patch)
        requests.Session.delete = _header_wrapper(requests.Session.delete)
