from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase

from w.django import utils
from w.tests.mixins.testcase_mixin import TestCaseMixin


class DjangoTestCase(TestCaseMixin, TestCase):
    """ For testing in Django Context """

    @staticmethod
    def get_request(url, data=None, method="get", **extra):
        request = RequestFactory()

        if method == "get":
            return request.get(url, data, **extra)
        return request.post(url, data, **extra)

    @staticmethod
    def add_user_permission(user, permission):
        """
        Add permission to user
        """
        permission = Permission.objects.get(codename=permission)
        user.user_permissions.add(permission)

    @staticmethod
    def reverse(url_name, params=None, query_params=None):
        """ "
        Url reverse with query string management

        Usage:
            self.reverse(
                'app.views.my_view',
                params={'pk': 123},
                query_kwargs={'key':'value', 'k2': 'v2'}
            )
        """
        return utils.reverse(
            viewname=url_name, kwargs=params, query_kwargs=query_params
        )
