from kitchenart import _logger

try:
    import kombu
    import msgpack
except ModuleNotFoundError:
    _logger.exception('This module requires django and rest_framework')
    raise
