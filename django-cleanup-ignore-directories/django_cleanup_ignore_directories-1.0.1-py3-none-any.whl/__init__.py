# coding: utf-8
'''
    django-cleanup automatically deletes files for FileField, ImageField, and
    subclasses. It will delete old files when a new file is being save and it
    will delete files on model instance deletion.
'''
from __future__ import unicode_literals

__version__ = '1.0.1'
default_app_config = 'django_cleanup_ignore_directories.apps.CleanupConfig'
