import random
from datetime import datetime
from typing import Union

import jwt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from sso_server.models import Token
from sso_server.utils import generate_random, time_slice

from basics.models import User


class TokenService(object):
	"""
	generate or get valid token for client
	"""
	
	def __init__(self, request):
		self.request = request
	
	@staticmethod
	def check_grant_type(grant_type: str) -> bool:
		"""
		check grant_type param for valid value
		"""
		if not grant_type and grant_type != 'authorization_code' and grant_type != 'refresh_token':
			return False
		else:
			return True
	
	@staticmethod
	def check_refresh_token(refresh_token: str) -> Union[bool, Token]:
		"""
		check refresh token for valid
		"""
		if not refresh_token:
			return False
		else:
			try:
				token = Token.objects.get(refresh=refresh_token, revoked=False)
				return token
			except ObjectDoesNotExist:
				return False
	
	@staticmethod
	def check_valid_token(access_token: str) -> Union[bool, Token]:
		"""
		check access token for valid
		"""
		try:
			token = Token.objects.get(access=access_token, revoked=False, valid_until__gt=datetime.now())
			return token
		except ObjectDoesNotExist:
			return False
	
	@staticmethod
	def get_user_info_by_token(access_token) -> dict:
		"""
		get user info and groups by token
		"""
		groups = []
		username = ''
		user_id = None
		is_active = None
		email = None
		
		header_access_token = ''
		
		try:
			if access_token.find('Bearer') > -1:
				try:
					header_access_token = access_token.split(' ')[1]
				except IndexError:
					pass
		except AttributeError:
			pass
		
		token = TokenService.check_valid_token(header_access_token)
		
		if token and isinstance(token, Token):
			if token.user.is_active:
				groups = [group.name for group in token.user.groups.all()]
				username = token.user.username
				user_id = token.user_id
				is_active = token.user.is_active
				email = token.user.email
		
		result = {
			'groups': groups,
			'username': username,
			'user_id': user_id,
			'is_active': is_active,
			'email': email
		}
		return result
	
	@staticmethod
	def make_new_token(user_id: int) -> Token:
		"""
		generate new pair of access and refresh tokens
		"""
		exp = time_slice()
		
		try:
			fullname = User.objects.get(pk=user_id).full_name()
		except ObjectDoesNotExist:
			fullname = ''
			
		payload = {
			'random': random.randint(1, 1000000),
			'user_id': user_id,
			'exp': exp,
			'fullname': fullname
		}
		access_token = jwt.encode(payload, 'access_secret', algorithm='HS256').decode('utf-8')
		
		token = Token()
		token.access = str(access_token)
		token.refresh = generate_random()
		token.user_id = int(user_id)
		token.valid_until = exp
		token.save()
		
		return token
	
	@staticmethod
	def revoke_token(client_id: str, user_id: int, token: str = None) -> None:
		"""
		revoke one token if set in params or all tokens for client
		"""
		if not token:
			tokens = Token.objects.filter(client_id=client_id)
			for token in tokens:
				token.revoked = True
				token.save()
		else:
			try:
				token = Token.objects.get(client_id=client_id, access=token, user_id=user_id)
				token.revoked = True
				token.save()
			except ObjectDoesNotExist:
				return
	
	def token(self, grant_type=None) -> Union[dict, bool]:
		"""
		return access token if everything is ok
		"""
		try:
			grant_type = self.request.POST['grant_type']
		except KeyError:
			grant_type = grant_type
			
		token = None

		if not TokenService.check_grant_type(grant_type):
			return False

		# return access token by authorization code
		if grant_type == 'authorization_code':
			# return old token if exist and valid or new token if doesn't exist
			try:
				token = Token.objects.get(user_id=self.request.user.id, revoked=False, valid_until__gt=datetime.now())
			except ObjectDoesNotExist:
				token = TokenService.make_new_token(self.request.user.id)
			except MultipleObjectsReturned:
				token = Token.objects.filter(user_id=self.request.user.id, revoked=False,
												valid_until__gt=datetime.now()).order_by('-id').first()

		# make new access token by refresh token
		if grant_type == 'refresh_token':
			token = TokenService.check_refresh_token(self.request.POST.get('refresh_token'))

			if not token:
				return False
			else:
				token.revoked = True
				token.save()
				
				token = TokenService.make_new_token(token.user.id)

		return {
			'access_token': token.access,
			'refresh_token': token.refresh
		}
