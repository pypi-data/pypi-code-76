import json

import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from sso_server.services.get_student_info import GetStudentInfo

parameters = pika.ConnectionParameters(**settings.RABBIT_PARAMS)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='sso_queue')

def callback(ch, method, properties, body):
	data = json.loads(body)
	
	if data.get('action') == 'student_info':
		# получение информации о студенте
		info = GetStudentInfo(data.get('user_id'))
		res = info.get_student_info_by_param(data.get('param'))
		routing_key = data.get('routing_key')
		
		ch.queue_bind(f'request-{routing_key}', exchange='amq.direct', routing_key=routing_key)
		ch.basic_publish(exchange='amq.direct',
							  routing_key=routing_key,
							  body=json.dumps(res),
							  properties=pika.BasicProperties(delivery_mode=2)
							  )

channel.basic_consume(queue='sso_queue', on_message_callback=callback, auto_ack=True)


class Command(BaseCommand):
	"""
	запуск консьюмера Rabbit
	"""
	def handle(self, *args, **options):
		channel.start_consuming()
