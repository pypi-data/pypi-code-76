from django.conf import settings
from .mixin import MiddlewareMixin

from ..router.utils import pin_this_thread, unpin_this_thread

# The name of the cookie that directs a request's reads to the master DB
PINNING_COOKIE = getattr(settings, 'TAMARIN_PINNING_COOKIE', 'tamarin_pin_writes')

# The number of seconds for which reads are directed to the master DB after a write
PINNING_SECONDS = int(getattr(settings, 'TAMARIN_PINNING_SECONDS', 10))

READ_ONLY_METHODS = frozenset(['GET', 'TRACE', 'HEAD', 'OPTIONS'])


class PinningRouterMiddleware(MiddlewareMixin):
    """
    Middleware to support the PinningReplicaRouter
    Attaches a cookie to a user agent who has just written, causing subsequent
    DB reads (for some period of time, hopefully exceeding replication lag)
    to be handled by the master.
    When the cookie is detected on a request, sets a thread-local to alert the
    DB router.
    """

    def process_request(self, request):
        """
        Set the thread's pinning flag according to the presence of the
        incoming cookie.
        """
        if PINNING_COOKIE in request.COOKIES or request.method not in READ_ONLY_METHODS:
            pin_this_thread()
        else:
            unpin_this_thread()

    def process_response(self, request, response):
        """For some HTTP methods, assume there was a DB write and set the
        cookie.
        Even if it was already set, reset its expiration time.
        """
        db_wrote = getattr(response, '_db_write', False)
        does_not_read_only_method = request.method not in READ_ONLY_METHODS
        if does_not_read_only_method or db_wrote:
            response.set_cookie(
                PINNING_COOKIE,
                value='y',
                max_age=PINNING_SECONDS
            )
        return response
