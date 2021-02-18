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

from confluent_kafka import Producer

from axualclient import patterns, ClientConfig

logger = logging.getLogger(__name__)


class AxualProducer(Producer):

    def __init__(self, disco: dict, app_config: ClientConfig, topic: str, config=None, *args, **kwargs):
        """
        Instantiate a producer for Axual. The _producer attribute is the
         confluent_kafka Producer class.

        Parameters
        ----------
        disco : dict
            Discovery API information
        app_config : ClientConfig
            App config information
        topic : str
            Name of the topic to produce to: <topicname>, for
             example:  TopicName
        config : dict, optional
            Additional configuration properties to set. For options, see
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Producer.

        """
        self.init_topic = topic
        self.init_config = config
        self.init_args = args
        self.init_kwargs = kwargs

        self.topic = patterns.resolve_topic(disco, topic)
        logger.debug(f"Full topic name: {self.topic}")

        self.configuration = {'bootstrap.servers': disco['bootstrap.servers'],
                              'security.protocol': 'SSL',
                              'ssl.ca.location': app_config.ssl_config.root_ca_location,
                              'ssl.key.location': app_config.ssl_config.private_key_location,
                              'ssl.certificate.location': app_config.ssl_config.certificate_location,
                             }

        if config is not None:
            self.configuration = {**self.configuration, **config}

        self._producer = Producer(self.configuration, *args, **kwargs)
        self.is_switching = False

    def delivery_report(self, err, msg):
        """
        Basic delivery report functionality. Logs to logger, user should
         have instantiated the root logger in their script to catch these
         messages.
        Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush().
        """
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.debug(f'Message (length {len(msg)}, starts with "{msg.value().decode("utf-8")[:min(10, len(msg))]}"'
                         f') delivered to topic {msg.topic()} partition [{msg.partition()}] offset [{msg.offset()}]')

    def produce(self, *args, callback=None, **kwargs) -> None:
        """
        Produce message to topic. Wrapper around confluent_kafka's
         Producer.produce() method.

        Parameters
        ----------
        callback : function, optional
            Callback function. The default (None) will use the default callback
             as defined by the delivery_report() method in this class.
        *args and **kwargs :
            Arguments to pass to Producer.produce(). value, key, ...

        Returns
        -------
        None.

        """
        if callback is None:
            callback = self.delivery_report

        while self.is_switching:
            sleep(1)
        return self._producer.produce(self.topic, *args, callback=callback, **kwargs)

    def __class__(self, *args, **kwargs): return self._producer.__class__(*args, **kwargs)
    def __dir__(self, *args, **kwargs): return self._producer.__dir__(*args, **kwargs)
    def __doc__(self, *args, **kwargs): return self._producer.__doc__(*args, **kwargs)
    def __eq__(self, *args, **kwargs): return self._producer.__eq__(*args, **kwargs)
    def __format__(self, *args, **kwargs): return self._producer.__format__(*args, **kwargs)
    def __ge__(self, *args, **kwargs): return self._producer.__ge__(*args, **kwargs)
    def __gt__(self, *args, **kwargs): return self._producer.__gt__(*args, **kwargs)
    def __hash__(self, *args, **kwargs): return self._producer.__hash__(*args, **kwargs)
    def __le__(self, *args, **kwargs): return self._producer.__le__(*args, **kwargs)
    def __len__(self, *args, **kwargs): return self._producer.__len__(*args, **kwargs)
    def __lt__(self, *args, **kwargs): return self._producer.__lt__(*args, **kwargs)
    def __ne__(self, *args, **kwargs): return self._producer.__ne__(*args, **kwargs)
    def __reduce__(self, *args, **kwargs): return self._producer.__reduce__(*args, **kwargs)
    def __reduce_ex__(self, *args, **kwargs): return self._producer.__reduce_ex__(*args, **kwargs)
    def __repr__(self, *args, **kwargs): return self._producer.__repr__(*args, **kwargs)
    def __sizeof__(self, *args, **kwargs): return self._producer.__sizeof__(*args, **kwargs)
    def __str__(self, *args, **kwargs): return self._producer.__str__(*args, **kwargs)
    def abort_transaction(self, *args, **kwargs): return self._producer.abort_transaction(*args, **kwargs)
    def begin_transaction(self, *args, **kwargs): return self._producer.begin_transaction(*args, **kwargs)
    def commit_transaction(self, *args, **kwargs): return self._producer.commit_transaction(*args, **kwargs)
    def flush(self, *args, **kwargs): return self._producer.flush(*args, **kwargs)
    def init_transactions(self, *args, **kwargs): return self._producer.init_transactions(*args, **kwargs)
    def list_topics(self, *args, **kwargs): return self._producer.list_topics(*args, **kwargs)
    def poll(self, *args, **kwargs): return self._producer.poll(*args, **kwargs)
    def send_offsets_to_transaction(self, *args, **kwargs): return self._producer.send_offsets_to_transaction(*args, **kwargs)
