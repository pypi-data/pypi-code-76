import logging
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.db.models.query import ModelIterable, QuerySet
from django.db.models.sql import Query
from requests import HTTPError
from rest_framework.exceptions import ValidationError

from django_urlqueryset.utils import get_default_params

logger = logging.getLogger(__name__)


class UrlModelIterable(ModelIterable):
    def __iter__(self):
        return self.queryset.deserialize(self.queryset._result_cache)


class UrlQuery:

    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.filters = {}
        self.order_by = []
        self.high_mark = settings.URLQS_HIGH_MARK
        self.low_mark = 0
        self.nothing = False
        self.distinct_fields = []

    def set_limits(self, low=None, high=None):
        if high is not None:
            if self.high_mark is not None:
                self.high_mark = min(self.high_mark, self.low_mark + high)
            else:
                self.high_mark = self.low_mark + high
        if low is not None:
            if self.high_mark is not None:
                self.low_mark = min(self.high_mark, self.low_mark + low)
            else:
                self.low_mark = self.low_mark + low

        if self.low_mark == self.high_mark:
            self.set_empty()

    def set_empty(self):
        self.nothing = True

    def clear_ordering(self, force_empty):
        self.order_by = []

    def add_ordering(self, *ordering):
        if ordering:
            self.order_by += ordering

    def clone(self):
        new = self.__class__(self.model)
        new.filters = self.filters.copy()
        new.high_mark = self.high_mark
        new.low_mark = self.low_mark
        new.nothing = self.nothing
        new.order_by = self.order_by
        return new

    def can_filter(self):
        return True

    def chain(self):
        return self.clone()

    def add_q(self, q_object):
        self.filters.update(dict(q_object.children))

    def _execute(self, request_params, method='get', **kwargs):
        query_params = {}
        if self.high_mark is not None:
            query_params['offset'] = self.low_mark
        if self.low_mark is not None:
            query_params['limit'] = self.high_mark - self.low_mark
        if self.order_by:
            query_params['ordering'] = ','.join(self.order_by)
        query_params.update(self.filters)
        for key, value in query_params.items():
            if key.endswith('__in') and isinstance(value, (list, tuple)):
                query_params[key] = ",".join(str(i) for i in value)
        _request_params = get_default_params()
        _request_params.update(request_params.copy())
        _request_params.update(kwargs)
        url = _request_params.pop('url').replace('{{model._meta.model_name}}', self.model._meta.model_name)
        if query_params:
            url = f"{url}?{urlencode(query_params, safe=',')}"
        response = getattr(requests, method)(url=url, **_request_params)
        response.raise_for_status()
        return response.json() if response.headers.get('Content-Type') == 'application/json' else response


class UrlQuerySet(QuerySet):

    def __init__(self, *args, **kwargs):
        self.request_params = kwargs.pop('request_params', {})
        super().__init__(*args, **kwargs)
        if isinstance(self.query, Query):
            self.query = UrlQuery(self.model)
        self._iterable_class = UrlModelIterable
        self._count = None
        self._result_cache = None

    def _clone(self):
        c = super()._clone()
        c.request_params = self.request_params
        return c

    def as_manager(cls, **request_params):
        from django.db.models.manager import Manager

        class _Manager(Manager.from_queryset(cls)):
            def get_queryset(self):
                queryset = super().get_queryset()
                queryset.request_params = self.request_params
                return queryset
        manager = _Manager()
        manager._built_with_as_manager = True
        manager.request_params = request_params
        return manager
    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)

    def count(self):
        if self._count is None:
            qs = self._chain()
            qs.query.set_limits(0, 1)
            return qs.query._execute(self.request_params)[settings.URLQS_COUNT]
        return self._count

    def _fetch_all(self):
        if self._count is None:
            response = self.query._execute(self.request_params)
            self._result_cache = list(self.deserialize(response[settings.URLQS_RESULTS]))
            self._count = response[settings.URLQS_COUNT]

    def create(self, **kwargs):
        try:
            response = self.query._execute(self.request_params, method='post', json=kwargs)
            return list(self.deserialize([response]))[0]
        except HTTPError as e:
            raise ValidationError({'remote_api_error': e.response.json()})

    def delete(self, **kwargs):
        try:
            response = self.query._execute(self.request_params, method='delete', json=kwargs)
            return response
        except HTTPError as e:
            raise ValidationError({'remote_api_error': e.response.json()})

    def update(self, **kwargs):
        return self._chain().query._execute(self.request_params, method='patch', json=kwargs)

    def deserialize(self, json_data=()):
        related_fields = {}
        for field in self.model._meta.fields:
            if field.related_model:
                related_fields[field.name] = {'manager': field.related_model.objects, 'pks': []}

        for obj_data in json_data:
            for field_name, value in related_fields.items():
                if field_name in obj_data and obj_data[field_name]:
                    related_fields[field_name]['pks'].append(obj_data[field_name])

        for rel_field, data in related_fields.items():
            if data['pks']:
                data['objs'] = {obj.pk: obj for obj in data['manager'].filter(pk__in=data['pks'])}

        for obj_data in json_data:
            obj = self.model()
            for field, value in obj_data.items():
                # if isinstance(value, list):
                #     value = next(iter(value), '')
                if value and field in related_fields.keys():
                    setattr(obj, field, related_fields[field]['objs'][value])
                else:
                    setattr(obj, field, value)
            yield obj

    def __getitem__(self, k):
        """Retrieve an item or slice from the set of results."""
        if not isinstance(k, (int, slice)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."

        # if self._result_cache is not None:
        #     return self._result_cache[k]

        if isinstance(k, slice):
            qs = self._chain()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.query.set_limits(start, stop)
            return list(qs)[::k.step] if k.step else qs

        qs = self._chain()
        qs.query.set_limits(k, k + 1)
        qs._fetch_all()
        return qs._result_cache[0]


