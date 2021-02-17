from typing import Dict

from firebase_admin import firestore, initialize_app, credentials, messaging
from ...connections.client import Client
from django.conf import settings
import datetime
import os

_DEFAULT_APP_NAME = 'MESSAGING_DEFAULT'


class MessagingClient(Client):
    __app__ = None

    __messaging_client__ = None

    __credential__ = credentials.Certificate(
        os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS',
            getattr(
                settings,
                'GOOGLE_APPLICATION_CREDENTIALS'
            )
        )
    )

    def _get_access_token(self):
        credential = self.__credential__
        access_token_info = credential.get_access_token()
        return access_token_info.access_token

    @staticmethod
    def create_notification(title, body) -> messaging.Notification:
        notification = messaging.Notification(
            title=title,
            body=body,
        )
        return notification

    @staticmethod
    def create_webpush(title, body, icon, actions=None) -> messaging.WebpushConfig:
        webpush = messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title=title,
                body=body,
                icon=icon,
                actions=actions
            )
        )
        return webpush

    @staticmethod
    def create_apns_config(priority, title, body, badge=30):
        apns_config = messaging.APNSConfig(
            headers={'apns-priority': str(priority)},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title=title,
                        body=body,
                    ),
                    badge=badge,
                ),
            ),
        )
        return apns_config

    @staticmethod
    def create_android_config(title, body, icon=None, color=None, priority='normal', action=None):
        """

        :param title:
        :param body:
        :param icon:
        :param color: #rrggbb format
        :param priority: default 'normal'
        :param action:
        :return:
        """
        android_config = messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority=priority,
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                icon=icon,
                color=color,
                click_action=action
            ),
        )
        return android_config

    @staticmethod
    def create_message(token=None, token_list=None, topic=None, condition=None, data: dict = None,
                       notification: messaging.Notification = None, webpush: messaging.WebpushConfig = None,
                       android: messaging.AndroidConfig = None, apns: messaging.APNSConfig = None):
        if token:
            message = messaging.Message(
                data=data,
                notification=notification,
                webpush=webpush,
                android=android,
                apns=apns,
                token=token,
            )
        elif token_list:
            message = messaging.MulticastMessage(
                data=data,
                notification=notification,
                webpush=webpush,
                android=android,
                apns=apns,
                tokens=token_list,
            )
        elif topic:
            message = messaging.Message(
                data=data,
                notification=notification,
                webpush=webpush,
                android=android,
                apns=apns,
                topic=topic,
            )
        elif condition:
            message = messaging.Message(
                data=data,
                notification=notification,
                webpush=webpush,
                android=android,
                apns=apns,
                condition=condition,
            )
        else:
            raise AttributeError("One of token, token_list, topic or condition should'nt None")

    @staticmethod
    def get_instance():
        return MessagingClient.__messaging_client__ or MessagingClient()

    def __init__(self):
        if MessagingClient.__messaging_client__:
            raise Exception("Messaging is singleton, just one instance")
        else:
            super(MessagingClient, self).__init__()
            credential = MessagingClient.__credential__
            options = getattr(settings, 'MESSAGING_APP_OPTIONS', None)
            name = getattr(settings, 'MESSAGING_APP_NAME', _DEFAULT_APP_NAME)
            app = initialize_app(credential=credential, options=options, name=name)
            MessagingClient.__app__ = app
            MessagingClient.__messaging_client__ = self

    def send(self, token=None, token_list=None, topic=None, condition=None, data: dict = None,
             notification: messaging.Notification = None, webpush: messaging.WebpushConfig = None,
             android: messaging.AndroidConfig = None, apns: messaging.APNSConfig = None, dry_run: bool = False):
        if token:
            return self._send_device(token, data, notification, webpush, android, apns, dry_run)
        elif token_list:
            return self.send_multicast(token_list, data, notification, webpush, android, apns, dry_run)
        elif topic:
            return self._send_to_topic(topic, data, notification, webpush, android, apns, dry_run)
        elif condition:
            return self.send_to_condition(condition, data, notification, webpush, android, apns, dry_run)
        else:
            raise AttributeError("One of token, token_list, topic or condition should'nt None")

    def _send_device(self, token, data: dict = None, notification: messaging.Notification = None,
                     webpush: messaging.WebpushConfig = None, android: messaging.AndroidConfig = None,
                     apns: messaging.APNSConfig = None, dry_run: bool = False):
        app = self.__app__
        message = messaging.Message(
            data=data,
            notification=notification,
            webpush=webpush,
            android=android,
            apns=apns,
            token=token,
        )
        response = messaging.send(
            message=message,
            dry_run=dry_run,
            app=app
        )
        return response

    def _send_to_topic(self, topic, data: dict = None, notification: messaging.Notification = None,
                       webpush: messaging.WebpushConfig = None, android: messaging.AndroidConfig = None,
                       apns: messaging.APNSConfig = None, dry_run: bool = False):
        app = self.__app__
        message = messaging.Message(
            data=data,
            notification=notification,
            webpush=webpush,
            android=android,
            apns=apns,
            topic=topic,
        )
        response = messaging.send(
            message=message,
            dry_run=dry_run,
            app=app
        )
        return response

    def send_to_condition(self, condition, data: dict = None, notification: messaging.Notification = None,
                          webpush: messaging.WebpushConfig = None, android: messaging.AndroidConfig = None,
                          apns: messaging.APNSConfig = None, dry_run: bool = False):
        """
        :param android:
        :param notification:
        :param data:
        :param dry_run:
        :param apns:
        :param webpush:
        :param condition: like "'stock' in topics || 'industry-tech' in topics"
        """
        app = self.__app__
        message = messaging.Message(
            data=data,
            notification=notification,
            webpush=webpush,
            android=android,
            apns=apns,
            condition=condition,
        )
        response = messaging.send(
            message=message,
            dry_run=dry_run,
            app=app
        )
        return response

    def subscribe_to_topic(self, topic: str, tokens: list):
        app = self.__app__
        response = messaging.subscribe_to_topic(tokens, topic, app)
        return response

    def unsubscribe_from_topic(self, topic: str, tokens: list):
        app = self.__app__
        response = messaging.unsubscribe_from_topic(tokens, topic, app)
        return response

    def send_all(self, messages, dry_run):
        """
        :param dry_run:
        :param messages: Create a list containing up to 500 messages
        :return:
        """
        app = self.__app__
        response = messaging.send_all(messages, dry_run, app)
        return response

    def send_multicast(self, tokens: list, data: dict = None, notification: messaging.Notification = None,
                       webpush: messaging.WebpushConfig = None, android: messaging.AndroidConfig = None,
                       apns: messaging.APNSConfig = None, dry_run: bool = False):
        """

        :param tokens: # Create a list containing up to 500 registration tokens.
        :param data:
        :param notification:
        :param webpush:
        :param android:
        :param apns:
        :param dry_run:
        :return:
        """
        app = self.__app__
        message = messaging.MulticastMessage(
            data=data,
            notification=notification,
            webpush=webpush,
            android=android,
            apns=apns,
            tokens=tokens,
        )
        response = messaging.send_multicast(message, dry_run, app)
        return response
