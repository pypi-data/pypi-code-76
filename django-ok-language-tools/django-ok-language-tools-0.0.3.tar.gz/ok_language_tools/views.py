from urllib.parse import unquote

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import translate_url
from django.utils.http import is_safe_url
from django.utils.translation import check_for_language

from .conf import REDIRECT_TO_QUERY_PARAMETER, LANGUAGE_QUERY_PARAMETER
from .utils import set_language_to_cookie_and_session

__all__ = (
    'set_language',
)


def set_language(request):
    """
    Redirect to a given URL while setting the chosen language in the session
    (if enabled) and in a cookie. The URL and the language code need to be
    specified in the request parameters.
    """
    redirect_to = request.GET.get(REDIRECT_TO_QUERY_PARAMETER)

    if (
            (redirect_to or not request.is_ajax())
            and not is_safe_url(
                url=redirect_to,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            )
    ):
        redirect_to = request.META.get('HTTP_REFERER')
        redirect_to = redirect_to and unquote(redirect_to)  # HTTP_REFERER may be encoded.

        if (
                not is_safe_url(
                    url=redirect_to,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                )
        ):
            redirect_to = '/'

    response = (
        HttpResponseRedirect(redirect_to)
        if redirect_to else HttpResponse(status=204)
    )

    lang_code = request.GET.get(LANGUAGE_QUERY_PARAMETER)

    if lang_code and check_for_language(lang_code):
        if redirect_to:
            redirect_to_trans = translate_url(redirect_to, lang_code)

            if redirect_to_trans != redirect_to:
                response = HttpResponseRedirect(redirect_to_trans)

        set_language_to_cookie_and_session(
            request=request,
            response=response,
            language=lang_code
        )

    return response
