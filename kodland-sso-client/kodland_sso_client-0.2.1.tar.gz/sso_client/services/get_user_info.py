import json
import uuid
from typing import Any

import pika
import requests
from django.conf import settings

from sso_client.send_message_to_rabbit import send_message_to_rabbit

# переменная для хранения результата промежуточных запросов
VALUE = {}


class GetUserInfo(object):
	"""
	request to sso server to get user's info
	"""
	
	@staticmethod
	def get_info(access_token: str) -> dict:
		url = f'{settings.SSO_URL}info'
		
		headers = {
			'Authorization': 'Bearer {}'.format(access_token)
		}
		
		response = requests.get(url, headers=headers)
		
		if response.status_code == 200:
			info = json.loads(response.text)
			return info
		else:
			return {}
		
	@staticmethod
	def return_response(ch, method, properties, body):
		"""
		обработчик сообщений из временной очереди
		"""
		ch.close()
		
		global VALUE
		VALUE = json.loads(body)
		
	@staticmethod
	def get_student_info_by_param(user_id: int, param_name: str) -> Any:
		url = f'{settings.SSO_URL}student_info'
		
		routing_key = str(uuid.uuid4())
		
		data = {
			'action': 'student_info',
			'user_id': user_id,
			'param': param_name,
			'routing_key': routing_key
		}
		
		if getattr(settings, 'RABBIT_ON', False):
			# общаемся с сервисом через rabbit
			# записываем в очередь
			send_message_to_rabbit(data, routing_key)
	
			# подписываемся на свою временную очередь
			parameters = pika.ConnectionParameters(**settings.RABBIT_PARAMS)
			connection = pika.BlockingConnection(parameters)
			
			channel = connection.channel()
	
			channel.basic_consume(queue=f'request-{routing_key}', on_message_callback=GetUserInfo.return_response, auto_ack=True)
			channel.start_consuming()
			
			global VALUE
			return VALUE.get('value')
		else:
			# общаемся с сервисом через http
			response = requests.post(url, data=data)

			if response.status_code == 200:
				info = json.loads(response.text)
				return info.get('value')
