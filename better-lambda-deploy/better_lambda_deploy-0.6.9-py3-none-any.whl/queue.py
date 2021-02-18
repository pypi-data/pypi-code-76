import boto3
import simplejson as json
import os


ENVIRONMENT = os.getenv("ENVIRONMENT")


class Queue(object):
    """
    An SQS queue. Any objects that inherit from this class will automatically be
    deployed as SQS queues.

    TODO: Maybe somehow add a message structure somehow, so that messages added to the
    queue can be validated against it?
    """

    def __init__(self):
        print(dir(self))
        # TODO: Figure out how to get the app name and environment in here. Do I need
        # some kind of context?
        self.queue_name = "legoon-" + self.__class__.__name__.lower() + "-prod"
        print(self.queue_name)
        print(f"Environment: {ENVIRONMENT}")
        if ENVIRONMENT == "sam":
            print("Using localstack for queues.")
            endpoint_url = "http://localstack:4566"
            self.client = boto3.client(
                "sqs", region_name="us-east-1", endpoint_url=endpoint_url
            )
        elif ENVIRONMENT == "local":
            print("Using localhost for queues.")
            endpoint_url = "http://localhost:4566"
            self.client = boto3.client(
                "sqs", region_name="us-east-1", endpoint_url=endpoint_url
            )
        else:
            self.client = boto3.client("sqs")

        self.queue_url = self.client.get_queue_url(QueueName=self.queue_name)[
            "QueueUrl"
        ]

    def add_message(self, message, trigger_time=None):
        """
        Add a message to the queue.
        """
        res = self.client.send_message(
            QueueUrl=self.queue_url, MessageBody=json.dumps(message)
        )
        print(res)

    def change_message_visibility(self, receipt_handle, visibility_timeout):
        res = self.client.change_message_visibility(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
            VisibilityTimeout=visibility_timeout,
        )
        print(res)

    def delete_message(self, receipt_handle):
        res = self.client.delete_message(
            QueueUrl=self.queue_url, ReceiptHandle=receipt_handle
        )
        print(res)
