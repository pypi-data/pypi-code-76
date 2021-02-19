import logging
import os

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from .identifier import JWTIdentifier

logger = logging.getLogger(__name__)


def alb_idp_auth_middleware(
    get_response, force_logout_if_no_header=True, region="ap-northeast-1"
):
    logger.debug("setup alb_idp_auth_middleware with %s" % (region,))
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if hasattr(settings, "AWS_REGION"):
        region = settings.AWS_REGION
    if not region:
        raise ImproperlyConfigured(
            "requires environment variable AWS_REGION,"
            " AWS_DEFAULT_REGION or settings.AWS_REGION."
        )

    def middleware(request):
        identifier = JWTIdentifier(region=region)
        info = identifier.identify(request)
        if info:
            logger.info(f"authenticated: {info}")
            request.META["REMOTE_USER"] = info["email"]
            request.META[f"{__name__}.user_claims"] = info
        return get_response(request)

    return middleware
