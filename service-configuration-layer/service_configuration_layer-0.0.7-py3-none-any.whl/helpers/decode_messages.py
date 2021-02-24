# Created by Antonio Di Mariano (antonio.dimariano@gmail.com) at 05/02/2021
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def decode_if_it_is_a_valid_json(string):
    try:
        return json.loads(string)
    except Exception as not_json:
        return string


def decode_incoming_msg(message):
    """
    if the message is already a JSON no decoding actions are needed.
    Otherwise the message will be decoded
    :param message:
    :return:
    """
    try:

        if type(message) is not dict:
            message = json.loads(message.decode('ascii'))
        for key in message:
            message[key] = decode_if_it_is_a_valid_json(message[key])
        return message
    except Exception as error:
        logger.error('Exception %s occurred decoding the incoming message %s \n' % (error, message))
        return 0
