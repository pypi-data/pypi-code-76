from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from sso_server.services.token_service import TokenService


class UserCookieMiddleWare(MiddlewareMixin):
	"""
	устанавливаем пару access/refresh токенов в куки, если пользователь авторизован
	удаляем эти куки, если пользователь не авторизован
	"""
	
	def process_response(self, request, response):
		if request.user.is_authenticated:
			token = TokenService(request)
			tokens = token.token(grant_type='authorization_code')
			
			response.set_cookie('access', tokens.get('access_token'), domain=settings.DOMAIN)
			response.set_cookie('refresh', tokens.get('refresh_token'), domain=settings.DOMAIN)
		
		return response
