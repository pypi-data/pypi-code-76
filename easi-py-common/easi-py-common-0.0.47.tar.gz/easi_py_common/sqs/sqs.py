import json
import time
import uuid

import boto3
import orjson
from botocore.config import Config

DEAD_QUEUE_NAME = 'easipay_letter_dead'
DEAD_QUEUE_NAME_FIFO = 'easipay_letter_dead.fifo'


def get_utc_timestamp():
    timestamp = time.time()
    return int(timestamp * 1000)


class SQSClient:
    __queue_map = {}
    __resource = None
    __dead_queue = None
    __dead_queue_fifo = None

    def __init__(self, region_name,
                 queue_name_prefix='',
                 aws_access_key_id='',
                 aws_secret_access_key='',
                 max_pool_connections=50,
                 max_attempts=3):
        self.queue_name_prefix = queue_name_prefix
        config = Config(
            region_name=region_name,
            signature_version='v4',
            max_pool_connections=max_pool_connections,
            retries={
                'max_attempts': max_attempts,
                # 'mode': 'standard'
            }
        )

        self.__client = boto3.client(service_name='sqs',
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     config=config)
        self.__init_queue()

    def send_message(self, queue_name, body, key='', group_id='', delay_seconds=0, cb=None):
        if '.fifo' in queue_name:
            if not group_id:
                raise Exception('MessageGroupId is required')

        return self.__send_message(queue_name, body, key, group_id, delay_seconds, cb, get_utc_timestamp())

    def set_queue_attributes(self, queue_url, attributes):
        self.__client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes=attributes)

    def get_queue_url(self, queue_name):
        url = self.__get_url_by_name(queue_name)
        return url

    def get_queue_attr(self, qurl, attr_names):
        return self.__client.get_queue_attributes(
            QueueUrl=qurl,
            AttributeNames=attr_names
        )

    def get_sqs_client(self):
        return self.__client

    def __init_queue(self):
        if len(self.queue_name_prefix) > 0:
            queue_data = self.__client.list_queues(QueueNamePrefix=self.queue_name_prefix)
        else:
            queue_data = self.__client.list_queues()

        if 'QueueUrls' in queue_data:
            for queue_url in queue_data['QueueUrls']:
                name = self.__get_name_by_url(queue_url)
                self.__queue_map[name] = queue_url

        if not self.__dead_queue:
            self.__install_dead(DEAD_QUEUE_NAME)
            self.__install_dead(DEAD_QUEUE_NAME_FIFO)

    def __get_name_by_url(self, q_url):
        return q_url[q_url.rindex('/') + 1:]

    def __get_url_by_name(self, queue_name):
        if queue_name not in self.__queue_map:
            qurl = self.__get_queue_url(queue_name)
            self.__queue_map[queue_name] = qurl
        return self.__queue_map[queue_name]

    def __send_message(self, queue_name, body, key='', group_id='', delay_seconds=0, cb=None,
                       send_start_time=get_utc_timestamp()):
        execute_start_time = get_utc_timestamp()
        work_wait_time = int(execute_start_time - send_start_time)
        msg_body = dict(
            t=execute_start_time,
            msg=body,
            key=key
        )
        try:
            queue_url = self.__get_queue_url(queue_name)

            if '.fifo' in queue_name:
                response = self.__client.send_message(
                    QueueUrl=queue_url,
                    MessageBody=json.dumps(msg_body),
                    MessageGroupId=str(group_id),
                    MessageDeduplicationId=str(uuid.uuid1())
                )
            else:
                if delay_seconds > 0:
                    if delay_seconds > 7200:
                        delay_seconds = 7200
                    msg_body['delay_seconds'] = delay_seconds

                if delay_seconds > 900:
                    delay_seconds = 900

                response = self.__client.send_message(
                    QueueUrl=queue_url,
                    DelaySeconds=delay_seconds,
                    MessageBody=json.dumps(msg_body),
                )

            msg_id = ''
            if 'MessageId' in response:
                msg_id = response['MessageId']

            if 'Code' in response:
                msg_id = response['Code']

            if cb:
                log_data = dict(
                    msg=msg_body['msg'],
                    t=msg_body['t'],
                    s_t=get_utc_timestamp(),
                    key=key,
                    group_id=group_id,
                    url=queue_url,
                    address=queue_name,
                    delay_seconds=msg_body['delay_seconds'] if 'delay_seconds' in msg_body else 0,
                    work_wait_time=work_wait_time
                )
                cb(msg_id, log_data)
                # self.__pool_work_log.submit(cb, msg_id, log_data)
            return True
        except Exception as e:
            if cb:
                log_data = dict(
                    msg=msg_body['msg'],
                    t=msg_body['t'],
                    s_t=get_utc_timestamp(),
                    key=key,
                    group_id=group_id,
                    url=e.message[0:254],
                    address=queue_name,
                    delay_seconds=msg_body['delay_seconds'] if 'delay_seconds' in msg_body else 0,
                    work_wait_time=work_wait_time,
                )

                cb('fail', log_data)
        return False

    def send_message_batch(self, queue_name, msgs, cb=None):
        if queue_name not in self.__queue_map:
            qurl = self.__get_queue_url(queue_name)
            self.__queue_map[queue_name] = qurl

        queue_url = self.__queue_map[queue_name]
        is_fifo = False
        if '.fifo' in queue_name:
            is_fifo = True

        entries = []
        for msg in msgs:
            if is_fifo:
                entries.append({
                    'MessageBody': orjson.dumps(msg['body']),
                    'MessageGroupId': str(msg['group_id']),
                    'MessageDeduplicationId': str(uuid.uuid1()),
                })
            else:
                delay_seconds = msg.get('delay_seconds', 0)
                if delay_seconds < 0:
                    delay_seconds = 0

                if delay_seconds > 0:
                    if delay_seconds > 7200:
                        delay_seconds = 7200

                if delay_seconds > 900:
                    delay_seconds = 900

                entries.append({
                    'MessageBody': orjson.dumps(msg['body']),
                    'DelaySeconds': delay_seconds

                })
        response = None
        try:
            response = self.__client.send_message_batch(QueueUrl=queue_url, Entries=entries)
        except Exception as e:
            if cb:
                cb('fail', {
                    'response': response,
                    'queue_url': queue_url,
                    'entries': entries
                })

    def __get_queue_url(self, queue_name, MessageRetentionPeriod=86400 * 3, receive_message_wait_time_seconds=10,
                        visibility_timeout=300, max_receive_count=6):
        if queue_name in self.__queue_map:
            return self.__queue_map[queue_name]

        try:
            queue = self.__client.get_queue_url(
                QueueName=queue_name,
            )
            if 'QueueUrl' in queue:
                return queue['QueueUrl']
        except:
            pass

        attributes = {
            'VisibilityTimeout': str(visibility_timeout),
            'DelaySeconds': '0',
            'MessageRetentionPeriod': str(MessageRetentionPeriod),
            'ReceiveMessageWaitTimeSeconds': str(receive_message_wait_time_seconds)
        }

        if '.fifo' in queue_name:
            attributes['FifoQueue'] = 'true'
            if self.__dead_queue_fifo:
                attributes['RedrivePolicy'] = json.dumps({
                    'deadLetterTargetArn': self.__dead_queue_fifo['arn'],
                    'maxReceiveCount': str(max_receive_count)
                })
        else:
            if self.__dead_queue:
                attributes['RedrivePolicy'] = json.dumps({
                    'deadLetterTargetArn': self.__dead_queue['arn'],
                    'maxReceiveCount': str(max_receive_count)
                })

        queue = self.__client.create_queue(
            QueueName=queue_name,
            Attributes=attributes
        )
        queue_url = queue['QueueUrl']
        return queue_url

    def __install_dead(self, dead_name):
        dead_queue_url = self.__get_queue_url(dead_name, MessageRetentionPeriod=86400 * 10)

        response = self.__client.get_queue_attributes(
            QueueUrl=dead_queue_url,
            AttributeNames=['QueueArn']
        )
        if '.fifo' in dead_name:
            self.__dead_queue_fifo = {'url': dead_queue_url, 'arn': response['Attributes']['QueueArn']}
        else:
            self.__dead_queue = {'url': dead_queue_url, 'arn': response['Attributes']['QueueArn']}
