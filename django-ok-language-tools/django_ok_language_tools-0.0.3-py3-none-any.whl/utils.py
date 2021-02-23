from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import translate_url
from django.utils import translation
from django.utils.translation.trans_real import language_code_prefix_re
from django.utils.translation import LANGUAGE_SESSION_KEY

__all__ = (
    'get_path_from_request',
    'force_translate_url',
    'get_language_from_cookie',
    'set_language_to_cookie_and_session',
    'is_url_translatable',
    'get_redirect_response_for_language'
)


def get_path_from_request(request) -> str:
    """
    Return current path from request, excluding language code
    """
    path = request.get_full_path()

    regex_match = language_code_prefix_re.match(path)

    if regex_match:
        lang_code = regex_match.group(1)
        languages = [
            language_tuple[0] for
            language_tuple in settings.LANGUAGES
        ]

        if lang_code in languages:
            path = path[1 + len(lang_code):]

            if not path.startswith('/'):
                path = '/' + path

    return path


def force_translate_url(url, language_code) -> str:
    prefix = f'/{language_code}/'

    if url.startswith(prefix):
        return url
    else:
        for lang_code, language in settings.LANGUAGES:
            prefix = f'/{lang_code}/'

            if url.startswith(prefix):
                url = url[len(prefix)-1:]
                break

        if language_code != settings.LANGUAGE_CODE:
            url = f'/{language_code}{url}'

    return url


def get_language_from_cookie(request) -> str:
    language = (
        request.get_signed_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            default=None
        )
    )

    return language


def set_language_to_cookie_and_session(
        request,
        response,
        language: str
):
    if hasattr(request, 'session'):
        request.session[LANGUAGE_SESSION_KEY] = language

    response.set_signed_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
    )


def is_url_translatable(url: str, language: str) -> bool:
    url = translate_url(url, language)
    return url.startswith(f'/{language}')


def get_redirect_response_for_language(
        language: str, request
) -> 'HttpResponse':
    translation.activate(language)
    request.LANGUAGE_CODE = language
    redirect_to = (
        force_translate_url(
            get_path_from_request(request),
            language
        )
    )
    response = HttpResponseRedirect(
        redirect_to=redirect_to
    )
    return response
