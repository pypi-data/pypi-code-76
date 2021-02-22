#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from cdumay_error.types import ValidationError
from flask_tat.base import BaseTATClient

CASCADE = ("nocascade", "cascade", "cascadeforce")


class TATClient(BaseTATClient):
    def message_list(self, topic, **kwargs):
        return self.client.do_request(
            method="GET", path="/messages/{}".format(topic.lstrip('/')),
            params=kwargs
        ).get('messages', list())

    def message_add(self, topic, text, **kwargs):
        data = dict(kwargs)
        data['text'] = text
        return self.client.do_request(
            method="POST", path="/message/{}".format(topic.lstrip('/')),
            data=data
        )

    def message_reply(self, topic, message_id, text):
        return self.client.do_request(
            method="POST", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="reply", text=text)
        )

    def message_like(self, topic, message_id):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="like")
        )

    def message_unlike(self, topic, message_id):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="unlike")
        )

    def message_label_add(self, topic, message_id, title, color):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(
                idReference=message_id, action="label", text=title, option=color
            )
        )

    def message_label_del(self, topic, message_id, title):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="unlabel", text=title)
        )

    def message_relabel(self, topic, message_id, labels):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="relabel", labels=labels)
        )

    def message_update(self, topic, message_id, text):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="update", text=text)
        )

    def message_concat(self, topic, message_id, text):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(
                idReference=message_id, action="concat",
                text=text if text.startswith(" ") else " %s" % text
            )
        )

    def message_move(self, topic, message_id):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(idReference=message_id, action="move")
        )

    def message_delete(self, message_id, cascade="nocascade"):
        if cascade not in CASCADE:
            raise ValidationError(message="Invalid cascade type", extra=dict(
                allowed=CASCADE, msgid="InvalidCascadeType",
                long_message="Invalid cascade type: '{}'".format(cascade)
            ))

        return self.client.do_request(
            method="DELETE", path="/message/{}/{}".format(cascade, message_id)
        )
