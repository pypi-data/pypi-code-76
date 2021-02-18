# pylint: skip-file
import ioc

from .services import APIMetadataService
from .services import HealthCheckService


def setup_ioc():
    ioc.provide('APIMetadataService', APIMetadataService())
    ioc.provide('HealthCheckService', HealthCheckService())
