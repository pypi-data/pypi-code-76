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

import json
import logging
from datetime import datetime
from threading import Thread
from time import sleep

import requests

from . import ClientConfig
from .AVROConsumer import AxualAVROConsumer
from .AVROProducer import AxualAVROProducer
from .Consumer import AxualConsumer
from .Producer import AxualProducer

logger = logging.getLogger(__name__)


class AxualClient:

    def __init__(self, client_config: ClientConfig):
        self._config = client_config
        self._discovered = None
        self._last_cluster = None
        self._producers = []
        self._AVROproducers = []
        self._consumers = []
        self._AVROconsumers = []

        self.stop_discovery = False
        self._disco_thread = Thread(target=self._continuous_discovery, daemon=True)
        self._disco_thread.start()

        while self._discovered is None:
            # Wait for discovery to finish before returning the client
            sleep(0.1)

    def _continuous_discovery(self):

        while not self.stop_discovery:
            self.discover()
            sleep(int(self._discovered['ttl']) / 1000)

    def discover(self):
        """
        Call Axual discovery API to get current cluster configuration

        Raises
        ------
        Exception
            When fetching the discovery API failed.

        Returns
        -------
        None, but sets self._discovered and self._lastCluster

        """

        headers = {'X-Application-Id': self._config._application_id,
                   'X-Application-Version': self._config._version,
                   'X-Client-Library': 'axual-python-client',
                   'X-Client-Library-Version': '0.0.1'  # TODO make dynamic
                   }

        params = {'applicationId': self._config._application_id,
                  'tenant': self._config._tenant,
                  'env': self._config._environment
                  }
        if not self._last_cluster is None:
            params = {**params, **{'lastCluster': self._last_cluster}}

        try:
            req = requests.get(url=self._config._endpoint,
                               headers=headers,
                               params=params,
                               verify=self._config.ssl_config.root_ca_location,
                               timeout=5)
        except Exception as e:
            logger.error(f"Could not fetch discovery API: {e}")
            raise

        self._discovered = json.loads(req.content)
        self._disco_timestamp = datetime.now()
        logger.debug(json.dumps(self._discovered, indent=2))

        if 'cluster' in self._discovered.keys():
            if not self._last_cluster == self._discovered['cluster'] and self._last_cluster is not None:
                logger.info(f"Need to switch clusters from {self._last_cluster} to {self._discovered['cluster']}!")
                self.switch_clusters()

            self._last_cluster = self._discovered['cluster']

    def switch_clusters(self):

        self.stop_discovery = True  # Stop discovery until all switches are complete

        thread_list = []
        for consumer in self._consumers:
            t = Thread(target=self.switch_consumer, args=(consumer,), daemon=True)
            thread_list.append(t)
            t.start()
        for consumer in self._AVROconsumers:
            t = Thread(target=self.switch_consumer, args=(consumer,), daemon=True)
            thread_list.append(t)
            t.start()
        for producer in self._producers:
            t = Thread(target=self.switch_producer, args=(producer, False,), daemon=True)
            thread_list.append(t)
            t.start()
        for producer in self._AVROproducers:
            t = Thread(target=self.switch_producer, args=(producer, True,), daemon=True)
            thread_list.append(t)
            t.start()

        logger.info(f"Switching started on {str(len(thread_list))} objects")

        for t in thread_list:
            t.join()
        logger.info("Switching complete on all objects!")
        self.stop_discovery = False  # Resume discovery

    def switch_consumer(self, consumer):
        consumer.is_switching = True
        poll_speed = consumer.poll_speed
        assignment = consumer.assignment()
        sleep(poll_speed)  # Wait outstanding polls before closing consumer
        consumer.close(with_pause=False)

        # Calculate switch time-out
        if len(assignment) > 0:
            # The default is AT_MOST_ONCE
            switch_timeout = max(int(self._discovered['distributor.timeout']) *
                                 int(self._discovered['distributor.distance']) -
                                 (datetime.now() - self._disco_timestamp).total_seconds() * 1000,
                                 int(self._discovered['ttl']))
            if consumer.configuration.get("auto.offset.reset") in ['earliest', 'smallest', 'begin', 'start']:
                # Strategy is AT_LEAST_ONCE
                switch_timeout = int(self._discovered['ttl'])

            sleep(switch_timeout / 1000)

        consumer.__init__(self._discovered, self._config,
                          consumer.init_topic_list,
                          config=consumer.init_config,
                          *consumer.init_args,
                          **consumer.init_kwargs
                          )

        consumer.poll_speed = poll_speed
        consumer.assign(assignment)

    def switch_producer(self, producer, is_avro: bool) -> None:
        producer.is_switching = True
        producer.flush()

        # Calculate switch time-out
        # The default is NOT KEEPING_ORDER
        switch_timeout = 0
        if producer.configuration.get("max.in.flight.requests.per.connection") in ['1', 1]:
            # Strategy is KEEPING_ORDER
            switch_timeout = (int(self._discovered['distributor.timeout']) *
                              int(self._discovered['distributor.distance']) -
                              (datetime.now() - self._disco_timestamp).total_seconds() * 1000)
        sleep(switch_timeout / 1000)

        if is_avro:
            producer.__init__(self._discovered, self._config,
                              producer.init_topic,
                              schema_value=producer.init_schema_value,
                              config=producer.init_config,
                              schema_key=producer.init_schema_key,
                              *producer.init_args, **producer.init_kwargs)
        else:
            producer.__init__(self._discovered, self._config,
                              producer.init_topic, config=producer.init_config,
                              *producer.init_args, **producer.init_kwargs)

    def get_consumer(self, topic_list, config=None, *args, **kwargs):
        self._consumers.append(AxualConsumer(self._discovered, self._config,
                                             topic_list, config=config, *args, **kwargs))
        return self._consumers[-1]

    def get_producer(self, topic, config=None, *args, **kwargs):
        self._producers.append(AxualProducer(self._discovered, self._config,
                                             topic, config=config, *args, **kwargs))
        return self._producers[-1]

    def get_avro_consumer(self, topic_list, config=None, from_value_dict=None, from_key_dict=None, *args, **kwargs):
        self._AVROconsumers.append(AxualAVROConsumer(self._discovered, self._config,
                                                     topic_list, config=config,
                                                     from_value_dict=from_value_dict,
                                                     from_key_dict=from_key_dict,
                                                     *args, **kwargs))
        return self._AVROconsumers[-1]

    def get_avro_producer(self, topic, schema_value=None,
                          config=None, schema_key=None, key_dict=None, value_dict=None, *args, **kwargs):
        self._AVROproducers.append(AxualAVROProducer(self._discovered, self._config,
                                                     topic, schema_value=schema_value,
                                                     config=config, schema_key=schema_key,
                                                     key_dict=key_dict, value_dict=value_dict,
                                                     *args, **kwargs))
        return self._AVROproducers[-1]
