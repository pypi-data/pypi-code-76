import json
import base64
import requests
from google.cloud import pubsub_v1
from expressmoney.api import Api
from expressmoney.dataclasses import Result, Status
from google.cloud import tasks_v2
import datetime


class PubSub:
    """Взаимодействие с сервисов Google Cloud Pub/Sub"""

    project_id = None
    topic_name = None

    def __init__(self, project_id, topic_name):

        self.project_id = project_id
        self.topic_name = topic_name

    @staticmethod
    def extract_message(message):
        """
        Извлекает данные из message
        """
        message_bytes = base64.b64decode(message['data'])
        message = json.loads(message_bytes)
        return message['data']['message']

    def publish_messages(self, messages, key=None):
        """
        Публикует message в сервис Google Cloud Pub/Sub
        """

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id, self.topic_name)

        for message in messages:
            message_bytes = self._create_message_body(message=message, key=key)
            try:
                publish_future = publisher.publish(topic_path, data=message_bytes)
                publish_future.result()  # Verify the publish succeeded
            except Exception as e:
                print(e)
                raise Exception

    @staticmethod
    def _create_message_body(message, key=None):

        if key:
            message_json = json.dumps({
                'data': {'message': message.get(key)},
            })
        else:
            message_json = json.dumps({
                'data': {'message': message},
            })

        return message_json.encode('utf-8')


class Functions(Status):
    """Взаимодействие Core c Cloud Functions"""

    def __init__(self, endpoint, api):

        self.core = Api(endpoint=endpoint)
        self.pubsub = PubSub(project_id='expressmoney', topic_name=endpoint)
        self.api = api

    def retrieve(self, data, headers=None):
        """Получение данных из стороннего сервиса с использованием REST API"""

        try:
            response = requests.post(self.api, headers=headers, json=data, timeout=(30, 30))
        except requests.exceptions.ConnectTimeout as error:
            raise error
        except requests.exceptions.ReadTimeout as error:
            raise error
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
        else:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))

    def update(self, message, context):
        """Для Event в статусе NEW вызывает _new для IN_PROCESS вызывает _in_process"""

        # Получаю pk(primary key) для объекта Event
        self._set_pk(self.pubsub.extract_message(message))

        # Получаю данные объекта Event по его pk
        self._set_event(self.core.retrieve(self.pk))

        # Обработка в зависимости от текущего статуса события
        if self.initial_event.get('status') == self.NEW:

            # Обнвляю статус на IN_PROCESS
            self.core.update(lookup_field=self.pk, status=Status.IN_PROCESS,
                             comment='Sets status from NEW to IN_PROCESS')

            # Обрабатываю событие
            result = self._new()

            # Сохраняю результат
            self.core.update(lookup_field=self.pk, status=result.status, comment=result.comment)

        elif self.initial_event.get('status') == self.IN_PROCESS:

            # Обрабатываю событие
            result = self._in_process()

            # Сохраняю результат
            self.core.update(lookup_field=self.pk, status=result.status, comment=result.comment)

        return self.SUCCESS, 200

    def _set_pk(self, pk):
        """pk(primary key) для объекта Event"""
        self.pk = pk

    def _set_event(self, event):
        """Данные объекта Event"""
        self.initial_event = event

    def _new(self):
        """Подготовка доменных данных и передача их в сервиса _service_new()"""

        user = Api('user')
        profile = Api('profile')
        user_obj = user.retrieve(self.initial_event.get('user'))
        profile_obj = profile.retrieve(self.initial_event.get('user'))
        data = {**user_obj, **profile_obj}

        return Result(self.SUCCESS, 'Demo result comment in _service_new()')

    def _in_process(self):
        """Подготовка доменных данных и передача их в сервиса _service_in_process()"""

        raise RuntimeError('Status IN_PROCESS недопустим для Event')


class Tasks(Status):
    """Работа с Google Cloud Tasks"""

    project = 'expressmoney'
    location = 'europe-west1'
    client = tasks_v2.CloudTasksClient()

    def __init__(self, endpoint, in_seconds=None, name=None):

        self.endpoint = endpoint

        self.parent = self.client.queue_path(self.project, self.location, queue=endpoint)

        self.payloads = Api(self.endpoint).list()

        self.task = {
            'app_engine_http_request': {
                'http_method': tasks_v2.HttpMethod.PUT,
                'relative_uri': '',
                'headers': {
                    'Content-type': 'application/json',
                },
            }
        }

        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
            # Add the timestamp to the tasks.
            self.task['schedule_time'] = timestamp

        if name:
            self.task['name'] = name  # 'my-unique-task'

    def create_tasks(self):

        for payload in self.payloads:

            # Convert dict to JSON string
            payload_string = json.dumps(payload)

            # The API expects a payload of type bytes.
            converted_payload = payload_string.encode()

            # Prepares task
            task = self.task
            task['app_engine_http_request']['body'] = converted_payload
            task['app_engine_http_request']['relative_uri'] = '/{}/{}/'.format(self.endpoint, payload.get('id'))

            self.client.create_task(parent=self.parent, task=task)

        return self.SUCCESS, 200
