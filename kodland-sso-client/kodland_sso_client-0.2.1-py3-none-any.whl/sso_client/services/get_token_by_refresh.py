import json
import requests
from django.conf import settings


class GetTokenByRefresh(object):
	"""
	request to sso server for get access token by refresh
	"""
	
	@staticmethod
	def get_token(refresh_token: str) -> dict:
		url = f'{settings.SSO_URL}token'
		
		data = {
			'grant_type': 'refresh_token',
			'refresh_token': refresh_token
		}
		
		response = requests.post(url, data=data)
		
		result = {}
		
		if response.status_code == 200:
			result = json.loads(response.text)
		
		return result
