"""Declares decorators to use with FastAPI RESt Framework."""
import functools

import ioc
import ioc.loader
from fastapi.responses import HTMLResponse


__all__ = [
    'action',
    'response_model',
    'spa',
]


class action:
    """Marks extra methods for routing."""

    def __init__(self, detail=False, name=None, methods=None):
        self.detail = detail
        self.name = name
        self.methods = methods or ['get']

    def __call__(self, func):
        self.name = self.name or func.__name__
        self.func = func
        func.action = self
        return func

    def add_to_app(self, app, base_path, cls):
        """Add the action to the FastAPI application."""
        base_path = str.rstrip(base_path, '/')
        if self.detail:
            base_path = f'{base_path}/{{resource_id}}'
        for method in self.methods:
            cls.as_method_handler(app, f'{base_path}/{self.name}',
                method, self.func.__name__)


def response_model(cls):
    """Decorates a request handler to use the given response model `cls`."""
    def decorator(func):
        func.response_model = cls
        return func
    return decorator


def spa(template, requires='TemplateService', path=None, detail=False):
    """Decorate a request handler to indicate that it returns a Single Page
    Application (SPA). The return value of the handler is expected to be
    a dictionary holding a template rendering context.
    """

    def decorator_factory(func):
        @functools.wraps(func)
        @action(name=path or func.__name__, detail=detail, methods=['get'])
        async def decorated(self, *args, **kwargs):
            svc = ioc.require(requires)
            ctx = await func(self, *args, **kwargs)
            ctx['kwargs'] = kwargs
            return HTMLResponse(await svc.render_to_string(template, ctx))

        decorated.response_class = HTMLResponse
        return decorated

    return decorator_factory
