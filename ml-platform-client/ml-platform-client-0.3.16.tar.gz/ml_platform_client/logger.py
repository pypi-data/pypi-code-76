import logging
import sys

from .context import request_context


class UuidFilter(logging.Filter):
    def filter(self, record):
        uuid = getattr(request_context, 'uuid', None)
        record.uuid = uuid
        return True


log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(process)d --- [%(threadName)s] %(filename)s:%(lineno)-4d: [ml-platform-client][%(uuid)s]%(message)s'
)
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(logging.INFO)
log.addFilter(UuidFilter())
log.propagate = False
