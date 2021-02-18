"""Declares :class:`HTTPStatusResource`."""
from fastapi import Response

from ..decorators import action
from ..dependency import Injected
from ..views import AnonymousResource


class HealthCheckResource(AnonymousResource):
    """Exposes endpoints for live- and readyness checks."""
    __module__ = 'frf.resources'
    resource_name = 'Health'

    @action(name='live', detail=False, methods=['get'])
    async def live(self,
        response: Response,
        check=Injected('HealthCheckService')
    ):
        """Perform a liveness check."""
        try:
            if not await check.is_live():
                response.status_code = 503
        except Exception: # pylint: disable=broad-except
            response.status_code = 503

    @action(name='ready', detail=False, methods=['get'])
    async def ready(self,
        response: Response,
        check=Injected('HealthCheckService')
    ):
        """Perform a readiness check."""
        try:
            if not await check.is_ready():
                response.status_code = 503
        except Exception: # pylint: disable=broad-except
            response.status_code = 503
