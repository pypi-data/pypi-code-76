"""Declares routers for API endpoints."""
import inspect


class FastAPIRouter:
    """A router implementation for use with FastAPI."""
    __module__ = 'frf'

    def __init__(self):
        self.endpoints = {}

    def add_to_app(self, app):
        """Add all endpoints to the ASGI application."""
        for name, cls in dict.items(self.endpoints):
            base_path = f'/{name}'

            # Iterate over all members of the class and find actions.
            for name, func in inspect.getmembers(cls):
                if not hasattr(func, 'action'):
                    continue
                func.action.add_to_app(app, base_path, cls)

            if hasattr(cls, 'create'):
                cls.as_method_handler(
                    app, f'{base_path}', 'POST', 'create')
            if hasattr(cls, 'retrieve'):
                cls.as_method_handler(
                    app, f'{base_path}/{{pk}}', 'GET', 'retrieve')
            if hasattr(cls, 'list'):
                cls.as_method_handler(
                    app, f'{base_path}', 'GET', 'list')
            if hasattr(cls, 'update'):
                cls.as_method_handler(
                    app, f'{base_path}/{{pk}}', 'PATCH', 'update')
            if hasattr(cls, 'delete'):
                cls.as_method_handler(
                    app, f'{base_path}/{{pk}}', 'DELETE', 'delete')
            if hasattr(cls, 'replace'):
                cls.as_method_handler(
                    app, f'{base_path}/{{pk}}', 'PUT', 'replace')

            app.include_router(cls.router,
                tags=[cls.resource_name or cls.__name__])

    def register(self, name, cls):
        """Register an endpoint under the given name.

        Args:
            name (:class:`str`): the name of the endpoint and base path
                relative to the API root.
            cls (:class:`~frf.GenericViewSet`): the viewset or endpoint to mount
                at the given base path.

        Returns:
            None
        """
        self.endpoints[name] = cls
