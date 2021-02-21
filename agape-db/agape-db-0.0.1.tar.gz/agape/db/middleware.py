from agape.request import set_request
from django.utils.deprecation import MiddlewareMixin

class AgapeUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        set_request(request)

    def process_response(self, request, response):
        set_request(None)
        return response

# class StackOverflowMiddleware(object):
#     def process_exception(self, request, exception):
#         return None