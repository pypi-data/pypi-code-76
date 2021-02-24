from typing import Any
from typing import List
from typing import Optional

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RedirectExceptionMiddleware(MiddlewareMixin):

    def process_exception(
        self,
        request: HttpResponse,
        exception: Exception,
    ) -> Optional[int]:
        from django import shortcuts

        if isinstance(exception, Redirect):
            if exception.error_message:
                messages.error(request, exception.error_message)
            if exception.args is not None:
                return shortcuts.redirect(reverse(exception.url_name, args=exception.args))
            else:
                return shortcuts.redirect(exception.url_name)


class Redirect(Exception):
    url_name: str
    error_message: Optional[str]
    args: List[Any]
    
    def __init__(self, url_name: str, error_message: str = None, args: List[Any] = None):
        self.url_name = url_name
        self.error_message = error_message
        self.args = args or []
