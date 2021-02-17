import time

from django.conf import settings


SESSION_EXPIRATION_SECONDS = getattr(settings, "SESSION_EXPIRATION_SECONDS", 3600)
SESSION_EXPIRATION_ACTIVITY_RESETS = getattr(
    settings, "SESSION_EXPIRATION_ACTIVITY_RESETS", True
)
SESSION_EXPIRATION_KEY = getattr(settings, "SESSION_EXPIRATION_KEY", "_last_active_at")


def has_session(request):
    return hasattr(request, "session") and not request.session.is_empty()


def session_expiration_middleware(get_response):
    """
    Middleware to expire Django sessions after a predetermined number of seconds has passed.
    """

    def middleware(request):
        if has_session(request):
            last_activity = request.session.get(SESSION_EXPIRATION_KEY)
            if (
                last_activity is None
                or time.time() - last_activity > SESSION_EXPIRATION_SECONDS
            ):
                request.session.flush()

        response = get_response(request)

        if has_session(request):
            last_activity = request.session.get(SESSION_EXPIRATION_KEY)
            if last_activity is None or SESSION_EXPIRATION_ACTIVITY_RESETS:
                request.session[SESSION_EXPIRATION_KEY] = time.time()

        return response

    return middleware
