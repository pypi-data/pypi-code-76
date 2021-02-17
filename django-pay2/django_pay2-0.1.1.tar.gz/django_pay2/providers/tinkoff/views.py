import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .exceptions import TinkoffNotifyValidationError
from .functions import get_tinkoff_api


@method_decorator(csrf_exempt, name="dispatch")
class NotifyView(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            print("JSON decode error")
            return HttpResponse("JSON decode error", status=400)
        api = get_tinkoff_api()
        try:
            result = api.notify(data)
        except TinkoffNotifyValidationError as exc:
            print(str(exc))
            return HttpResponse(str(exc), status=400)

        result.payment.accept()
        return HttpResponse("OK")
