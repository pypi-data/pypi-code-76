"""
admin.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2/2/21 10:53 AM
"""

from django.utils.translation import gettext_lazy as _
from django.contrib.admin import ModelAdmin, site

from . import models


class CkfinderResource(ModelAdmin):
    """
    Ckfinder 资源
    """

    list_display = (
        'name',
        'adapter',
        'max_size',
        'path',
        'url',
        'allowed_extensions',
        'denied_extensions',
        'enabled',
        'verify_permissions'
    )
    list_filter = ('adapter', 'enabled', 'verify_permissions')
    search_fields = ('name', 'adapter')

    fieldsets = (
        (_('基础配置'), {
            'fields': (
                'adapter',
                'name',
                'path',
                'url',
                'enabled',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('上传限制'), {
            'fields': (
                'allowed_extensions',
                'denied_extensions',
                'max_size',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('权限管理'), {
            'fields': (
                'verify_permissions',
                'ck_finder_file_create',
                'ck_finder_file_delete',
                'ck_finder_file_rename',
                'ck_finder_file_view',
                'ck_finder_folder_create',
                'ck_finder_folder_delete',
                'ck_finder_folder_rename',
                'ck_finder_folder_view',
                'ck_finder_image_resize',
                'ck_finder_image_resize_custom',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('其他配置'), {
            'fields': (
                'other',
            ),
            'classes': ('extrapretty', 'wide')
        }),
    )


if not site.is_registered(models.CkfinderResource):
    site.register(models.CkfinderResource, CkfinderResource)
