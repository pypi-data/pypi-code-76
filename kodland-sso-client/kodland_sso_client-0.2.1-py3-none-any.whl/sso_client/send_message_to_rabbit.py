import json

import pika
from django.conf import settings


def send_message_to_rabbit(message: dict, routing_key: str) -> None:
	"""
	отправка сообщения в Rabbit
	"""
	parameters = pika.ConnectionParameters(**settings.RABBIT_PARAMS)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	
	channel.queue_declare(queue=f'request-{routing_key}', auto_delete=True)
	channel.queue_bind('sso_queue', exchange='amq.direct', routing_key=routing_key)
	
	channel.basic_publish(exchange='amq.direct',
	                      routing_key=routing_key,
	                      body=json.dumps(message),
	                      properties=pika.BasicProperties(delivery_mode=2)
	                      )
	
	connection.close()
