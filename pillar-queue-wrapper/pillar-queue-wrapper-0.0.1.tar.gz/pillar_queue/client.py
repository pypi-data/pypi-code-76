import sys
import logging
import uuid
import time

import boto3
from botocore.exceptions import ClientError


class Queue:
    def __init__(self, name, aws_access_key=None, aws_access_secret=None, aws_default_region='us-east-1'):
        '''
        Initializes the class. The variable `name` is the name of the queue as seen on AWS. 

        The variables `aws_access_key` and `aws_access_secret` correspond to the variables `aws_access_key_id` and `aws_secret_access_key` from within boto3.
        If these variables are not set, boto3 will get your credentials as detailed [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

        The default region set by this library is `us-east-1`. To change that, simply set `aws_default_region` to the region string, for example `us-east-2` or `eu-
        '''
        self.name = name
        self.aws_access_key = aws_access_key
        self.aws_access_secret = aws_access_secret
        self.aws_default_region = aws_default_region

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

        self.response = None
        self.fifo = '.fifo' in self.name
        self.attributes = None

        self.wait_for_accuracy = False
        self.wait_time = 60

        if aws_access_key and aws_access_secret:
            self.sqs_resource = boto3.resource(
                service_name='sqs',
                region_name=self.aws_default_region,
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_access_secret
            )
        else:
            self.sqs_resource = boto3.resource(service_name='sqs')

        if aws_access_key and aws_access_secret:
            self.sqs_client = boto3.client(
                service_name='sqs',
                region_name=self.aws_default_region,
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_access_secret
            )
        else:
            self.sqs_client = boto3.client(service_name='sqs')

        self.url = self.sqs_client.get_queue_url(
            QueueName=self.name)['QueueUrl']
        self.queue = self.sqs_resource.get_queue_by_name(QueueName=self.name)

    def __eq__(self, other):
        '''
        Returns whether or not 2 queues have the same name.
        '''
        return self.name == other.name

    def __len__(self):
        '''
        Get approximate length of the queue. See [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.get_queue_attributes) for more info.
        
        Set `q.wait_for_accuracy = True` to have this function block for 60 seconds while the AWS queueing service updates itself to get a more up to date value.
        '''
        attribute = 'ApproximateNumberOfMessages'

        if self.wait_for_accuracy:
            time.sleep(self.wait_time)

        self.attributes = self.sqs_client.get_queue_attributes(
            QueueUrl=self.url,
            AttributeNames=[attribute]
        )
        length = self.attributes['Attributes'].get(attribute)
        return int(length)

    def receive_message(self, wait_time=10, delete_message=True):
        """
        Get a message from the queue. 

        The variable `wait_time` is how long it waits in seconds before returning `None` if the queue is empty. The minimum `wait_time` is 1 second.

        By default, the message received is deleted from the queue when gotten, as this library assumes you will be
        processing the message upon receiving it. If you do not want to do this, you can instead set `delete_message` to `False`,
        preventing the message from being deleted from the queue. To later delete the message, see [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.delete).
        """
        messages = self._receive_messages(
            max_number=1, wait_time=wait_time, delete_messages=delete_message)

        if len(messages) == 1:
            message = messages[0]
            return message

        return None

    def _receive_messages(self, max_number=10, wait_time=10, delete_messages=True):
        '''
        Gets multiple messages with a max of `10`. Also defaults to getting `10` messages. 

        To get a specific number of messages, set `max_number` to a number in the range `[1, 10]`.

        The variable `wait_time` specifies how long the function will wait in seconds before returning an empty list of messages. It will also wait if the queue does not contain the requested number of messages. The minimum `wait_time` is 1 second.

        By default, all of the messages are deleted from the queue when getting them, as this library assumes you will be 
        processing them immediately upon receiving them. If you do not want to do this, you can instead set `delete_messages` to `False`,
        preventing the messages from being deleted from the queue. To later delete those messages, see [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.delete).
        '''
        try:
            messages = self.queue.receive_messages(
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
        except ClientError as e:
            self.logger.error(e)
            return []
        except Exception as e:
            raise e

        if delete_messages:
            for message in messages:
                message.delete()

        return messages

    def wait_for_message(self, delete_message=True):
        """
        Blocking function that waits for a message to appear in the specified(via init function) queue. 

        Returns the single message that it received from the queue. 

        By default, the message received is deleted from the queue when gotten, as this library assumes you will be
        processing the message upon receiving it. If you do not want to do this, you can instead set `delete_message` to `False`,
        preventing the message from being deleted from the queue. To later delete the message, see [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.delete).
        """

        self.logger.info('Waiting for queue item.')
        message = None
        while message is None:
            message = self.receive_message()
        return message

    def send_message(self, message, message_attributes={}, message_group_id=None, deduplication_id=None):
        '''
        Sends a message to the queue. The body of the message is housed in the `message` variable. 

        Information about `message_attributes` can be found [here](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-java-send-message-with-attributes.html).

        The following variables are only relevant if you are using a FIFO Queue on AWS SQS. More information about the type of queue can be found [here](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html).

        Information about `deduplication_id` can be found [here](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html). By default a random one is used to allow for all messages to be added to the queue.

        Information about `message_group_id` can be found [here](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html).
        '''

        try:
            if self.fifo:

                if not message_group_id:
                    message_group_id = __name__
                if not deduplication_id:
                    deduplication_id = uuid.uuid1().hex
                self.response = self.queue.send_message(
                    MessageBody=message,
                    MessageAttributes=message_attributes,
                    MessageDeduplicationId=deduplication_id,
                    MessageGroupId=message_group_id
                )
            else:
                self.response = self.queue.send_message(
                    MessageBody=message,
                    MessageAttributes=message_attributes,
                )
        except ClientError as e:
            self.logger.error(e)
            return False
        except Exception as e:
            raise e

        return True

    def purge(self):
        '''
        Purges all messages from the queue. WARNING: This can be a dangerous function to execute as all items will be purged regardless of the state of any other programs accessing
        the queue. 
        This function will also purge all items added to the queue for 60 seconds from the function call.
        This function is blocking for those 60 seconds.
        '''
        try:
            self.queue.purge()
            time.sleep(61)
            return True
        except Exception as e:
            self.logger.error(e)
        return False
