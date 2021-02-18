# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
from time import sleep

from confluent_kafka import Consumer

from axualclient import patterns, ClientConfig

logger = logging.getLogger(__name__)


class AxualConsumer(Consumer):
    """Simple balanced consumer class.
    Implements __iter__ to be able to create a for loop on the consumer
     to iterate through messages: for msg in AxualConsumer. Set pause
     attribute to break from loop.
    Set poll_speed attribute to change the polling speed (default: 0.2 [secs])."""

    def __init__(self, disco: dict, app_config: ClientConfig, topic_list, config: dict = None, *args, **kwargs):
        """
        Instantiate a consumer for Axual. Derives from confluent_kafka
         Consumer class.
        Note that auto-commit is set to False, so received messages must
         be committed by your script's logic.

        Parameters
        ----------
        disco : dict
            Discovery API information
        app_config : ClientConfig
            App config information
        topic_list : str, or list of str
            List of names of the topic(s) to consume from:
                <topicname>
             for example:  ['TopicName', 'OtherTopic']
        config : dict, optional
            Additional configuration properties to set. For options, see
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md`
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Consumer.
        """
        self.init_topic_list = topic_list
        self.init_config = config
        self.init_args = args
        self.init_kwargs = kwargs

        if isinstance(topic_list, str):
            topic_list = [topic_list]
        if not isinstance(topic_list, list):
            raise Exception("topic_list argument must be a list!")
        self.topic_list = [patterns.resolve_topic(disco, topic)
                           for topic in topic_list]
        logger.debug(f"Full topic names: {self.topic_list}")

        self.configuration = {'bootstrap.servers': disco['bootstrap.servers'],
                              'security.protocol': 'SSL',
                              'ssl.ca.location': app_config.ssl_config.root_ca_location,
                              'ssl.key.location': app_config.ssl_config.private_key_location,
                              'ssl.certificate.location': app_config.ssl_config.certificate_location,
                              'group.id': patterns.resolve_group(disco, app_config._application_id),
                              }

        if config is not None:
            self.configuration = {**self.configuration, **config}

        super().__init__(self.configuration, *args, **kwargs)

        self.subscribe(self.topic_list)
        self.poll_speed = 0.2
        self.pause = False
        self.is_switching = False

    def __iter__(self):
        """Continuously loop through messages until self.pause is set to True"""
        self.pause = False
        while not self.pause:
            msg = self.poll(self.poll_speed)
            yield msg

    def poll(self, poll_speed=None):
        if poll_speed is None:
            poll_speed = self.poll_speed
        while self.is_switching:
            # Don't hang the program, just return None as if there was no new message
            sleep(poll_speed)
            return None
        return super().poll(poll_speed)

    def close(self, with_pause=True):
        # Make sure background threads are killed before closing
        self.pause = with_pause
        super().close()
