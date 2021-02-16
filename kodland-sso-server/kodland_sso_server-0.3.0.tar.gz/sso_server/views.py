from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from sso_server.services.get_student_info import GetStudentInfo
from sso_server.services.token_service import TokenService


# Create your views here.
class UserDataView(APIView):
	"""
	получение данных пользователя по токену
	"""
	
	def get(self, request):
		"""
		Получение базовых данных о пользователе
		В заголовке запроса нужно передать HTTP_AUTHORIZATION Bearer {access_token}
		"""
		result = TokenService.get_user_info_by_token(request.META.get('HTTP_AUTHORIZATION'))
		return Response(result, status=HTTP_200_OK)
	
	
class GetStudentInfoView(APIView):
	"""
	получение данных студента
	
	HTTP_200_OK
	"""
	
	def post(self, request):
		result = GetStudentInfo(request.POST.get('user_id'))
		return Response(
			result.get_student_info_by_param(request.POST.get('param')), status=HTTP_200_OK
		)
	

class TokenView(APIView):
	"""
	return access token to user if everything is ok
	"""
	
	def post(self, request):
		"""
		Получение пары access/refresh токенов.
		Используется для обновления access по истечению срока годности токена по refresh.
		
		В теле запроса необходимо передать дополнительные параметры:
		grant_type=authorization_code/refresh_token

		В ответе вернётся JSON:
		{
			"access_token": "{access_token}",
			"token_type": "bearer",
			"refresh_token": "{refresh_token}"
		}
		
		HTTP_200_OK - успех
		HTTP_400_BAD_REQUEST - некорректные параметры
		"""
		token = TokenService(request)
		
		result = token.token()
		
		if isinstance(result, dict):
			return Response(result, status=HTTP_200_OK)
		else:
			return Response({'error': 'Invalid params'}, status=HTTP_400_BAD_REQUEST)
