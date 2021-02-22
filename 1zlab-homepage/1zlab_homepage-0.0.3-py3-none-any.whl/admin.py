from django.contrib import admin

from .models import *


# Register your models here.

class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ["title", "rank", "img_url"]
    list_editable = ["rank"]
    search_fields = ["title", "rank"]


admin.site.register(HomePageThumbnail, ThumbnailAdmin)
