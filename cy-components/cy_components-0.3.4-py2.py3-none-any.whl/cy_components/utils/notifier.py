import logging
import json
import requests
from datetime import datetime
from enum import IntEnum


class MessageType(IntEnum):
    DingDing = 0
    WeChatWork = 1


class MessageHandler:

    @staticmethod
    def __send_wechatwork_msg(content, token):
        """发送企业微信通知"""
        logger = logging.getLogger('MessageHandler.WechatWork')
        logger.setLevel(logging.INFO)
        logger.info(content)
        try:
            msg = {
                "msgtype": "markdown",
                "markdown": {"content": content + '\n>' + datetime.now().strftime("%m-%d %H:%M:%S")}
            }
            Headers = {"Content-Type": "application/json ;charset=utf-8 "}
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + token
            body = json.dumps(msg)
            requests.post(url, data=body, headers=Headers, timeout=15)
        except Exception as err:
            logger.error('Send WechatWork message failed: %s', format(repr(err)))

    @staticmethod
    def __send_dingding_msg(title, content, token):
        """send meesage by dingding"""
        logger = logging.getLogger('MessageHandler.Dingding')
        logger.setLevel(logging.INFO)
        logger.info(content)
        try:
            msg = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content + '\n>' + datetime.now().strftime("%m-%d %H:%M:%S")
                }
            }
            Headers = {"Content-Type": "application/json ;charset=utf-8 "}
            url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
            body = json.dumps(msg)
            requests.post(url, data=body, headers=Headers, timeout=15)
        except Exception as err:
            logger.error('Send Dingding message failed: %s', format(repr(err)))

    @staticmethod
    def send_message(msg, title='Message', type=MessageType.DingDing, token=None):
        """Send simple message"""
        if type == MessageType.DingDing:
            MessageHandler.__send_dingding_msg(title, msg, token)
        elif type == MessageType.WeChatWork:
            MessageHandler.__send_wechatwork_msg(msg, token)
