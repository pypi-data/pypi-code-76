from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from .utils import generate_random, time_slice


# Create your models here.
class Token(models.Model):
	"""
	пара access/refresh токенов
	"""
	access = models.TextField(verbose_name='Access token', db_index=True, unique=True)
	refresh = models.TextField(verbose_name='Refresh token', default=generate_random)
	created_at = models.DateTimeField(verbose_name='Дата и время создания', default=now)
	valid_until = models.DateTimeField(verbose_name='Срок годности до', default=time_slice)
	revoked = models.BooleanField(verbose_name='Отозван', default=False)
	user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, verbose_name='Пользователь')
	
	def __str__(self):
		return '{} ({})'.format(str(self.user.username), str(self.created_at))
	
	class Meta:
		verbose_name = 'Access/Refresh Token'
		verbose_name_plural = 'Access/Refresh Tokens'
