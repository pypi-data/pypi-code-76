import os

RBX_ENV = os.getenv('RBX_ENV', 'dev')
RBX_PROJECT = f'{RBX_ENV}-platform-eu'

GOOGLE_PROJECT = os.getenv('GOOGLE_PROJECT')

MDM_PUBSUB_TOPIC = os.getenv('GOOGLE_PUBSUB_TOPIC', 'platform-notifications')
MDM_PAYLOAD_VERSION = 2

AWS_BUCKET = os.getenv('AWS_BUCKET')
AWS_REGION = os.getenv('AWS_REGION')
