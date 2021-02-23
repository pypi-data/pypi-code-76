import json
from django.shortcuts import HttpResponse


class ApiHome:

    __registered = None

    def __init__(self):
        self.__registered = ApiFunctionList()

    def register(self):

        def wrapper(func):

            name = func.__name__

            # Check for existing names
            if hasattr(self.__registered, name):
                raise ValueError(f'{name} is already registered.')

            # Check format
            if not name.startswith("api_get_") and not name.startswith("api_post_"):
                raise ValueError(f'{name} must begin with api_get_ or api_post_')

            # Add
            api_function = ApiFunction(func)
            self.__registered.register(name, api_function)

            return func

        return wrapper

    def run_api_function(self, request):

        # Get Action Name
        if request.method == "POST":
            body = json.loads(request.body.decode("utf-8"))
            action_name = body.get('action_name', 'None')
        elif request.method == "GET":
            action_name = request.GET.get("action_name", 'None')
        else:
            action_name = "None"

        # Build Function Name
        func = f'api_{request.method}_{action_name}'.lower().replace('-', '_')

        # Attempt Function
        if hasattr(self.__registered, func):
            return getattr(self.__registered, func).func(request)
        else:
            return self.error(f'Unknown function: {action_name}')

    def parse_body(self, request):
        return json.loads(request.body.decode("utf-8"))

    def error(self, message='', status_code=400):
        data = {'message': message}
        return self.api(data, False, status_code)

    def api(self, data=None, success=True, status_code=200):
        data = data if data is not None else {}
        content = json.dumps({'data': data, 'success': success}, indent=None, separators=(',', ':'))
        return HttpResponse(content=content, content_type='application/json', status=status_code)


class ApiFunctionList:
    def register(self, name, api_function):
        setattr(self, name, api_function)


class ApiFunction:

    func = None
    name = None

    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __str__(self):
        return self.name


api = ApiHome()


def get_pagination(items_count, current_page=1, per_page=50):

    current_page = int(current_page)
    remainder = items_count % per_page
    number_of_pages = int(((items_count - remainder) / per_page) + min(1, remainder))
    current_page = min(max(1, current_page), number_of_pages)

    offset_start = max((current_page - 1) * per_page, 0)
    offset_end = max(min(offset_start + per_page, items_count), 0)

    return {
        'items_count': items_count,
        'number_of_pages': number_of_pages,
        'current_page': current_page,
        'offset_start': offset_start,
        'offset_end': offset_end,
        'per_page': per_page,
    }
