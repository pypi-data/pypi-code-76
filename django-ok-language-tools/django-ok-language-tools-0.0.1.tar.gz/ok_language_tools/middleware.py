from django.http.response import HttpResponse
from django.utils import translation

from .conf import (
    REDIRECT_EXCLUDE_PREFIXES,
    DEFAULT_REDIRECT_LANGUAGE,
    VISITED_SESSION_KEY
)
from .utils import (
    get_language_from_cookie,
    set_language_to_cookie_and_session,
    is_url_translatable,
    get_redirect_response_for_language
)

__all__ = (
    'language_redirect_middleware',
)


def language_redirect_middleware(get_response):
    """
    Middleware to redirect to default language
    """
    def middleware(request):
        response: 'HttpResponse' = get_response(request)
        current_language: str = translation.get_language()
        cookie_language: str = get_language_from_cookie(request)
        was_visited: str = (
            request.session.pop(
                VISITED_SESSION_KEY,
                request.META.get('HTTP_REFERER')
            )
        )

        is_skip: bool = (
            not is_url_translatable(
                url=request.path,
                language=DEFAULT_REDIRECT_LANGUAGE
            )
            or request.path.startswith(
                REDIRECT_EXCLUDE_PREFIXES
            )
            or response.status_code == 404
        )

        if is_skip:
            return response

        is_first_visit = (
            cookie_language is None
            and current_language != DEFAULT_REDIRECT_LANGUAGE
        )

        if is_first_visit:
            new_language = DEFAULT_REDIRECT_LANGUAGE
            response = (
                get_redirect_response_for_language(
                    language=new_language,
                    request=request
                )
            )

        elif cookie_language and current_language != cookie_language:
            if not bool(was_visited):
                new_language = cookie_language
            else:
                new_language = current_language

            response = (
                get_redirect_response_for_language(
                    language=new_language,
                    request=request
                )
            )
            request.session[VISITED_SESSION_KEY] = (
                request.build_absolute_uri(request.path)
            )

        else:
            new_language = current_language

        if cookie_language != new_language:
            set_language_to_cookie_and_session(
                request=request,
                response=response,
                language=new_language
            )

        return response

    return middleware
