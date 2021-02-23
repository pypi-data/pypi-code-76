from . import api


def api_view(request):
    return api.run_api_function(request)
