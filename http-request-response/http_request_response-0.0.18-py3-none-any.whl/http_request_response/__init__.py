import traceback
from datetime import datetime
from functools import wraps
import copy

import requests
from flask import current_app as app
from flask import request, has_request_context
from flask_jwt_extended import get_jwt_identity
from http_status_code.standard import bad_request


class RequestResponse:

    def __init__(self, status_code=None, data=None, message=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)

    def update(self, status_code=200, data=None, message=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)

    def __message_to_str(self, message):
        return message if message is None else str(message)

    def __call__(self, *args, **kwargs):
        return self.__dict__


class RequestUtilities:
    @staticmethod
    def get_request_context():
        context = dict()
        if has_request_context():
            context['url'] = request.url
            context['remote_addr'] = request.remote_addr
            context['method'] = request.method

            # Query string args
            try:
                context['qs_args'] = request.qs_args
            except:
                context['qs_args'] = {}

            # Body args
            try:
                for key in list(request.body_args.keys()):
                    if 'password' in key or 'db_uri' in key:
                        request.body_args.pop(key, None)
                context['body_args'] = request.body_args

                # Pop any file bytes
                dict(request.body_args).pop('file_bytes', None)
            except Exception as e:
                context['body_args'] = {}

            # Claims
            try:
                context['claims'] = request.claims
            except:
                context['claims'] = {}

        return context

    @staticmethod
    def update_status_message(status, msg):
        # Update the status mesaage
        if app.config.get('SHOW_EXCEPTION'):
            status.update_msg(msg)
        else:
            # Do not return the Exception to the user, on the prouction server
            status.update_msg(f'Something went wrong. '
                              f'Our technical team is doing their best to take care of it.')

    @staticmethod
    def pop_password():
        try:
            if 'password' in request.args:
                request.args.pop('password')

            if 'password' in request.json:
                request.json.pop('password')
        except:
            return

    @classmethod
    def try_except(cls, fn):
        """A decorator for all of the actions to do try except"""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            status = bad_request
            request_context = {}
            data = {}

            try:
                status, data = fn(*args, **kwargs)
                if app.config.get('LOG_INFO'):
                    try:
                        request_context = RequestUtilities.get_request_context()
                    except Exception as e:
                        NotifcationManager.send('Request Context failed.')

                    try:
                        app.app_info_logger.info(request_context)
                    except Exception as e:
                        NotifcationManager.send('INFO Logger failed.')

                    # pop password from args
                    cls.pop_password()

                    if status.code == 410:

                        # Format a message
                        msg = f"{datetime.utcnow()} UTC." \
                              f"\n{app.config.get('APPLICATION_NAME')}" \
                              f"\n{app.config.get('ENV_NAME')}." \
                              f"\n\nIP: {request.remote_addr}" \
                              f"\nURL: {request.url}" \
                              f"\nMethod: {request.method}" \
                              f"\n\nStatus code: {status.code}" \
                              f"\nStatus message: {status.message}" \
                              f"\n\nQs args\n{request.args}" \
                              f"\n\nBody args:\n{request.json}" \
                              f"\n\nRequest context:\n{request_context}" \
                              f"\n\nArgs validation response:\n{data}"

                        # Log status code 410 as an exception
                        try:
                            app.app_exc_logger.exception(msg)
                        except:
                            NotifcationManager.send('Logger failed. Status code 410')

                        # Notification
                        try:
                            NotifcationManager.send(msg)
                        except Exception as e:
                            app.app_exc_logger.exception('Notification manager failed. Status code 410')

                        # Update the status message
                        RequestUtilities.update_status_message(status, data)

            except Exception as exc:
                full_traceback = traceback.format_exc()

                # Update the status message
                RequestUtilities.update_status_message(status, exc)

                # pop password from args
                cls.pop_password()

                # Format a message
                msg = f"{datetime.utcnow()} UTC." \
                      f"\n{app.config.get('APPLICATION_NAME')}" \
                      f"\n{app.config.get('ENV_NAME')}." \
                      f"\n\nIP: {request.remote_addr}" \
                      f"\nURL: {request.url}" \
                      f"\nMethod: {request.method}" \
                      f"\n\nQs args\n{request.args}" \
                      f"\n\nBody args:\n{request.json}" \
                      f"\n\nRequest context:\n{request_context}" \
                      f"\n\nException: {exc}" \
                      f"\nException type: {type(exc)}" \
                      f"\n\nFull Traceback:\n{full_traceback}"

                try:
                    app.app_exc_logger.exception(msg)
                except Exception as e:
                    NotifcationManager.send('EXC Logger failed')

                try:
                    NotifcationManager.send(msg)
                except Exception as e:
                    app.app_exc_logger.exception('Notification manager failed. Bad request.')

            rs = RequestResponse(status_code=status.code, message=status.message, data=data)
            return rs()

        return wrapper


class NotifcationManager:

    @staticmethod
    def send(msg):
        NotifcationManager.notify_telegram(msg)
        NotifcationManager.notify_slack(msg)

    @staticmethod
    def notify_telegram(msg):
        try:
            url = app.config['TELEGRAM_API_URL']
            chat_id = app.config['TELEGRAM_CONV_ID']
        except:
            return
        payload = {'text': msg, 'chat_id': chat_id}
        requests.post(url=url, json=payload)

    @staticmethod
    def notify_slack(msg):
        try:
            url = app.config['SLACK_API_URL']
        except:
            return
        payload = {'text': msg}
        requests.post(url=url, json=payload)
