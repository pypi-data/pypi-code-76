from django.contrib import admin
from .models import Token


# Register your models here.
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
	"""
	manage Refresh/Access tokens
	"""
	list_display = ('user', 'access', 'refresh', 'created_at', 'valid_until', 'revoked')
	list_filter = ('user',)
	search_fields = ['user__email']
	list_display_links = ('user', 'access')
