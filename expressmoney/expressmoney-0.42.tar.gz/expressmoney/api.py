import requests
from .dataclasses import Status


class Api:
    api = "https://expressmoney.ew.r.appspot.com/{}/"

    def __init__(self, endpoint):
        self.api = self.api.format(endpoint)

    def list(self):
        """
        Возвращает список объектов из ИС Expressmoney
        """
        return self._response()

    def retrieve(self, lookup_field):
        """
        Возвращает один объект из ИС Expressmoney
        """
        return self._response(lookup_field=lookup_field)

    def update(self, lookup_field, status, comment):
        """
        Обновляет значения полей Status и Comment сущности Event Core
        """

        if status not in [Status.NEW, Status.IN_PROCESS, Status.SUCCESS, Status.FAILURE, Status.ERROR, Status.CANCEL]:
            raise RuntimeError('Статус должен быть равен NEW, INPR, SCS, FAIL, ERROR', 'CANCEL')

        data = {
            'status': status,
            'comment': str(comment)[:255],
        }

        return self._response(data=data, lookup_field=lookup_field, method='put')

    def _get_url(self, lookup_field=None):
        if lookup_field:
            return self.api + str(lookup_field) + '/'
        else:
            return self.api

    def _response(self, data=None, lookup_field=None, method='get'):

        url = self._get_url(lookup_field=lookup_field)

        if method == 'put':
            response = requests.put(url, json=data)
        elif method == 'post':
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
        elif response.status_code == 404:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Object Not Found'))
        else:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))
