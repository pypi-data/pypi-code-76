from tamarin.rest.router import OptionalSlashRouter
from .api import ReportApi

router = OptionalSlashRouter()

router.register('log', ReportApi, 'log')
