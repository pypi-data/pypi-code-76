from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        setattr(self, 'count', self.get_count(queryset))
        return super(Pagination, self).paginate_queryset(queryset, request, view)

    def get_count(self, queryset):
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)

    def get_paginated_response(self, data):
        return Response({
            'current': self.page.number,
            'count': getattr(self, 'count', '-'),
            **data
        })
