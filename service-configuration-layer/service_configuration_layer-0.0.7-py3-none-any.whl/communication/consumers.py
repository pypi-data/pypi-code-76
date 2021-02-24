# Created by Antonio Di Mariano (antonio.dimariano@gmail.com) at 12/01/2021
from confluent_kafka import KafkaError
import os
import datetime
from datetime import datetime, timezone
from service_configuration_controller.helpers.decode_messages import decode_incoming_msg
from service_configuration_controller.helpers.confluent_kafka_configuration_builder import \
    build_consumer_configuration_from_os_env_vars
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s:%(message)s',
    level=logging.INFO
)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)


def request_service_configuration(kafka_producer_instance, monitoring_producer_instance,service_name, initial):
    """
    This method produces a message using the given kafka_producer_instance.
    The purpose of the message is to request a configuration file for the service.
    The timer of 2 seconds needs to avoid sending messages faster than how the consumer can receive a response.

    :param kafka_producer_instance:
    :param service_name:
    :param initial:
    :return:
    """
    if not initial:
        time.sleep(3)

        logger.info(
            'Requesting configuration for service name %s' % service_name)

        kafka_producer_instance.produce_message(value={"service_name": service_name, 'application': 'trialcloud',
                                                       'timestamp': datetime.now(timezone.utc).replace(
                                                           microsecond=0).isoformat()})
        monitor_operation(monitoring_producer_instance, service_name)

        return 1
    else:

        # print('no need')
        return 0


def monitor_operation(monitoring_producer_instance, service_name):
    message = {"service_name": service_name, 'application': 'trialcloud',
               'configuration_requested': 1,
               'configuration_retrieved': 0,
               'timestamp': datetime.now(timezone.utc).replace(
                   microsecond=0).isoformat()}
    monitoring_producer_instance.produce_message(value=message)


def set_configuration(service_conf_to_store, abs_path_to_configuration_directory=None):
    """
    This method writes the given dicti service_conf_to_store to the abs_path_to_configuration_directory
    :param service_conf_to_store:
    :return:
    """

    from service_configuration_controller.helpers.operation_with_files import write_data_to_json_file

    if abs_path_to_configuration_directory is None:
        configuration_file = os.path.abspath('configuration') + '/service_configuration.json'
    else:
        configuration_file = abs_path_to_configuration_directory + '/service_configuration.json'
    return write_data_to_json_file(data_to_persit=service_conf_to_store, filename=configuration_file)


def init_consumer_with_schema_registry(configuration_from_env, group_id, offset):
    """
    This method creates an instance of AvroConsumer
    :param configuration_from_env:
    :param group_id:
    :param offset:
    :return:
    """
    from confluent_kafka.avro import AvroConsumer
    consumer_conf = build_consumer_configuration_from_os_env_vars(configuration_from_env=configuration_from_env,
                                                                  group_id=group_id, offset=offset)
    return AvroConsumer(consumer_conf)


def init_consumer(configuration_from_env, group_id, offset):
    """
    This method creates an instance of Consumer
    :param configuration_from_env:
    :param group_id:
    :param offset:
    :return:
    """
    from confluent_kafka import Consumer
    consumer_conf = build_consumer_configuration_from_os_env_vars(configuration_from_env=configuration_from_env,
                                                                  group_id=group_id, offset=offset)
    return Consumer(**consumer_conf)


class ConfigurationConsumer:

    def __init__(self, **kwargs):
        self.service_name = kwargs.get('service_name')
        self.consumer_topic = kwargs.get('topic')
        consumer_configuration = kwargs.get('configuration_from_env')
        if consumer_configuration.get('schema_registry_url'):
            self.consumer = init_consumer_with_schema_registry(
                configuration_from_env=kwargs.get('configuration_from_env'), group_id=kwargs.get('group_id'),
                offset=kwargs.get('offset'))
        else:
            self.consumer = init_consumer(configuration_from_env=kwargs.get('configuration_from_env'),
                                          group_id=kwargs.get('group_id'), offset=kwargs.get('offset'))

        self.service_conf_requester_instance = kwargs.get('service_conf_requester_instance')
        self.monitoring_producer_instance = kwargs.get('monitoring_producer_instance')
        self.initial = kwargs.get('initial', 0)
        self.just_listen = kwargs.get('just_listen', 0)
        self.lets_start = 0

    def run(self):
        if not self.just_listen:
            msg = 'Services Configuration Tool v2.0.0 [Requesting Configuration Mode Enabled ✔] %s \n' % self.consumer_topic
        elif self.just_listen:
            msg = 'Services Configuration Tool v2.0.0 [Listener Mode Enabled ✔] %s \n' % self.consumer_topic
        logger.info(msg)

        try:
            self.consumer.subscribe(self.consumer_topic, on_assign=self.print_assignment)

            while True:

                incoming_message = self.consumer.poll(1)
                if incoming_message is None:
                    if self.lets_start and not self.just_listen and not request_service_configuration(
                            service_name=self.service_name,
                            initial=self.initial,
                            kafka_producer_instance=self.service_conf_requester_instance,monitoring_producer_instance=self.monitoring_producer_instance):
                        break
                    continue
                elif incoming_message.error() is None:
                    message_payload = decode_incoming_msg(message=incoming_message.value())

                    if message_payload.get('service_name') == self.service_name:
                        message = {"service_name": self.service_name, 'application': 'trialcloud',
                                   'configuration_requested': 1,
                                   'configuration_retrieved': 1,
                                   'timestamp': datetime.now(timezone.utc).replace(
                                       microsecond=0).isoformat()}
                        if set_configuration(service_conf_to_store=message_payload):
                            self.initial = 1
                        else:
                            message['configuration_retrieved'] = 0
                            self.initial = 0
                        self.monitoring_producer_instance.produce_message(value=message)


                elif incoming_message.error():
                    if incoming_message.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.error('%% %s [%d] reached end at offset %d\n' %
                                     (incoming_message.topic(), incoming_message.partition(),
                                      incoming_message.offset()))
                    elif incoming_message.error():
                        logger.error(
                            '[' + datetime.now(timezone.utc).replace(
                                microsecond=0).isoformat() + '] Consumer Error {incoming_message.error()}\n')
                        continue


        except Exception as whatever_it_is:
            logger.error(
                '[' + datetime.now(timezone.utc).replace(
                    microsecond=0).isoformat() + '] EXCEPTION %s on the consumer for topic(s) %s\n' % (
                    whatever_it_is, self.consumer_topic))
            exit(1)

        finally:
            self.consumer.close()


    def print_assignment(self, consumer, partitions):
        logger.info(
            'Consumer %s Topic:%s  Assignment:%s' % (
                consumer,self.consumer_topic, partitions))
        self.lets_start = 1
