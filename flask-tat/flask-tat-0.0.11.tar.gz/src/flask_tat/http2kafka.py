#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from cdumay_rest_client.client import RESTClient
from flask_tat.base import BaseTATClient


class HTTP2KafkaClient(BaseTATClient):
    def message_add(self, topic, **kwargs):
        return self.client.do_request(
            method="POST", path="/message/{}".format(topic.lstrip('/')),
            data=kwargs, parse_output=False
        )

    def message_reply(self, topic, tag_ref, text):
        return self.client.do_request(
            method="POST", path="/message/{}".format(topic.lstrip('/')),
            data=dict(text=text, tagReference=tag_ref, action="reply"),
            parse_output=False
        )

    def message_relabel(self, topic, tag_ref, labels):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data=dict(labels=labels, tagReference=tag_ref, action="relabel"),
            parse_output=False
        )

    @property
    def client(self):
        if self._client is None:
            self._client = RESTClient(
                server=self.app.config['TAT_URL'],
                headers={
                    "X-Tat_username": self.app.config["TAT_USERNAME"],
                    "X-Tat_password": self.app.config["TAT_PASSWORD"],
                    "Content-type": "application/json",
                },
                ssl_verify=self.app.config["TAT_SSL_VERIFY"],
            )
        return self._client
