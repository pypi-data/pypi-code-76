# coding: utf-8
'''
    AppConfig for django-cleanup, prepare the cache and connect signal handlers
'''
from __future__ import unicode_literals

from django.apps import AppConfig

from . import cache, handlers


class CleanupConfig(AppConfig):
    name = 'django_cleanup_ignore_directories'
    verbose_name = 'Django Cleanup Ignore Directories'

    def ready(self):
        cache.prepare()
        handlers.connect()
