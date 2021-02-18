"""Provides the functions to create the ASGI application."""
import inspect
import logging
import warnings

import fastapi
import unimatrix.runtime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ioc.exc import UnsatisfiedDependency
from starlette.middleware.trustedhost import TrustedHostMiddleware
from unimatrix.conf import settings
from unimatrix.ext.model.exc import CanonicalException
from unimatrix.ext.model.exc import FeatureNotSupported

from .resources import HealthCheckResource
from .resources import ServiceMetadataResource
from .routers import FastAPIRouter


logger = logging.getLogger('endpoints')
DEFAULT_ROUTER = FastAPIRouter()
DEFAULT_SECRET_KEY = '0' * 64


def _ensure_secret_key():
    try:
        settings.SECRET_KEY
    except AttributeError:
        warnings.warn(
            "CAUTION: The SECRET_KEY setting is not specified, using the "
            "default of {DEFAULT_SECRET_KEY}."
        )
        os.environ['SECRET_KEY'] = DEFAULT_SECRET_KEY


class FastAPI(fastapi.FastAPI):
    """A :class:`fastapi.FastAPI` subclass that provides integration with
    the Unimatrix Framework.
    """
    endpoints = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.endpoints is None:
            self.endpoints = DEFAULT_ROUTER

    def add_resource_router(self, router):
        """Add a :class:`~frf.FastAPIRouter` to the ASGI application."""
        router.add_to_app(self)

    def add_resource(self, cls, base_path=None):
        """Add a RESTFUL API resource `cls` to the default router."""
        app = self
        if base_path is None:
            base_path = f'/{cls.get_resource_name()}'
        if not base_path:
            base_path = '/'
        if not str.startswith(base_path, '/'):
            base_path = f'/{base_path}'

        # Iterate over all members of the class and find actions.
        for _, func in inspect.getmembers(cls):
            if not hasattr(func, 'action'):
                continue
            func.action.add_to_app(app, base_path, cls)

        if hasattr(cls, 'create'):
            cls.as_method_handler(
                app, f'{base_path}', 'POST', 'create')
        if hasattr(cls, 'retrieve'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'GET', 'retrieve')
        if hasattr(cls, 'list'):
            cls.as_method_handler(
                app, f'{base_path}', 'GET', 'list')
        if hasattr(cls, 'update'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'PATCH', 'update')
        if hasattr(cls, 'delete'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'DELETE', 'delete')
        if hasattr(cls, 'replace'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'PUT', 'replace')

        self.include_router(cls.router,
            tags=[cls.resource_name or cls.__name__])

        cls.asgi = self


async def _handle_canonical_exception(request, exc):
    if isinstance(exc, UnsatisfiedDependency):
        return await _handle_canonical_exception(request, FeatureNotSupported())
    if isinstance(exc, CanonicalException):
        if exc.http_status_code >= 500:
            exc.log(logger.exception)
        return JSONResponse(
            status_code=exc.http_status_code,
            content=exc.as_dict()
        )
    else:
        raise NotImplementedError


def get_asgi_application(allowed_hosts=None, **kwargs):
    """Return a :class:`fastapi.FastAPI` instance. This is the main ASGI
    application.

    The :func:`get_asgi_application()` gathers configuration from various
    sources in order to configure a basic :class:`fastapi.FastAPI` instance. The
    order is as defined below:

    - :attr:`unimatrix.conf.settings` - this module loads all uppercased
      variables in the Python module (or package) indicated by the environment
      variable ``UNIMATRIX_SETTINGS_MODULE`` (see below).
    - :mod:`unimatrix.environ`

    All common environment variables specified by the Unimatrix Framework are
    detected by :func:`get_asgi_application()`. Additional configuration may
    be provided by setting the environment variable
    ``UNIMATRIX_SETTINGS_MODULE``, holding the qualified name of a Python
    module. See also :ref:`index-environment-variables`.
    """
    app = FastAPI(
        openapi_url=getattr(settings, 'OPENAPI_URL', '/openapi.json'),
        docs_url=getattr(settings, 'DOCS_URL', '/'),
        exception_handlers={
            CanonicalException: _handle_canonical_exception,
            UnsatisfiedDependency: _handle_canonical_exception
        }
    )
    _ensure_secret_key()
    if settings.HTTP_CORS_ENABLED:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.HTTP_CORS_ALLOW_ORIGINS,
            allow_credentials=settings.HTTP_CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.HTTP_CORS_ALLOW_METHODS,
            allow_headers=settings.HTTP_CORS_ALLOW_HEADERS,
            expose_headers=settings.HTTP_CORS_EXPOSE_HEADERS,
            max_age=settings.HTTP_CORS_TTL
        )

    # Always enable the TrustedHostMiddleware.
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=(
            allowed_hosts or getattr(settings, 'HTTP_ALLOWED_HOSTS', [])
        )
    )

    app.add_resource(HealthCheckResource, base_path='.well-known/health')
    app.add_resource(ServiceMetadataResource, base_path='.well-known/self')

    @app.on_event('startup')
    async def on_startup():
        await unimatrix.runtime.on('boot')

    @app.on_event('shutdown')
    async def on_shutdown():
        await unimatrix.runtime.on('shutdown')

    return app
