from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _


# Create your models here.
class OauthUser(AbstractBaseUser, PermissionsMixin):
	identifier = models.CharField(max_length=250, unique=True)
	
	email = None
	is_staff = None
	is_active = None
	is_superuser = None
	is_anonymous = True
	
	groups = models.ManyToManyField(
		Group,
		verbose_name=_('groups'),
		blank=True,
		related_name="oauth_user_set",
		related_query_name="oauth_user"
	)
	
	user_permissions = models.ManyToManyField(
		Permission,
		verbose_name=_('user permissions'),
		blank=True,
		related_name="oauth_user_set",
		related_query_name="oauth_user"
	)
	
	USERNAME_FIELD = 'identifier'
	
	def __str__(self):
		return self.identifier
	
	def has_module_perms(self, app_label):
		if self.is_superuser:
			return True
		
		permissions = self.user_permissions.all()
		return app_label in [f'{permission.content_type.app_label}' for permission in permissions]
	
	def has_perm(self, perm, obj=None):
		if self.is_superuser:
			return True
		
		permissions = self.user_permissions.all()
		return perm in [f'{permission.content_type.app_label}.{permission.codename}' for permission in permissions]
