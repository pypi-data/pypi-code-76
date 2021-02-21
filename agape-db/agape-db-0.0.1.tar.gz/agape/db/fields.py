from django.db import models
from django.conf import settings
from .request import get_user
from agape.string import slugify


""" User field with 'auto' and 'auto_add' options."""
class UserField(models.ForeignKey):

	def __init__( self, on_delete, **kwargs ):

		self.auto = kwargs.pop('auto', False)
		self.auto_add = kwargs.pop('auto_add', False)

		kwargs['on_delete'] = on_delete
		kwargs['to'] = settings.AUTH_USER_MODEL

		super().__init__(**kwargs)

	def pre_save( self, instance, add ):
		current_value = self.value_from_object( instance )
		user = get_user()

		# set the attribute to the current user
		if user.pk:
			if self.auto or (self.auto_add and add and not current_value):
				setattr( instance, self.name, user )

		return super().pre_save(instance, add)



class SlugField(models.SlugField):


	def __init__(self, *args, **kwargs ):
		self.from_field = kwargs.pop('from_field', None)
		super().__init__(*args, **kwargs)


	def pre_save( self, instance, add ):
		current_value = self.value_from_object( instance )

		if add and not current_value:
			source_value = self.from_field.value_from_object( instance )
	
			if not source_value == None:
				value = slugify( source_value )
				setattr( instance, self.name, value)


