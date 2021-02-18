"""Declares :class:`HealthCheckService`."""


class HealthCheckService:
    """Exposes an API to perform health checks. The
    :class:`HealthCheckService` makes the distinction between two types of
    health checks.

    A **readyness** check indicates if the application is ready to serve
    traffic. If a readyness check fails, the deployment infrastructure may
    choose to stop sending traffic to the application.

    A **liveness** check indicates if the application is alive or dead. A
    failing liveness check may result in the application process being
    killed.

    :class:`HealthCheckService` is injected with the name ``HealthCheckService``
    using the :mod:`ioc` module. To customize the behavior of the health checks,
    a subclass may be provided by injecting it at application startup:

    .. code:: python

        import frf

        from myproject import MyHealthCheckService


        app = frf.get_asgi_application()

        @app.on_event('startup')
        async def boot():
            frf.provide('HealthCheckService',
                MyHealthCheckService(), force=True)
    """

    async def is_live(self) -> bool:
        """Return a boolean indicating if the application is live."""
        return True

    async def is_ready(self) -> bool:
        """Return a boolean indicating if the application is ready."""
        return True
