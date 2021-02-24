# Created by Antonio Di Mariano (antonio.dimariano@gmail.com) at 12/01/2021
import threading
import os
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from confluent_kafka_producers_wrapper.producer import Producer

logger = logging.getLogger()
default_headers = {"Content-Type": "application/json"}
logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO
)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)


def wait_to_retrieve_service_configuration(service_name=os.environ.get('service_name')):
    """
    topic_for_setting_conf=tc-set-service-configuration
    topic_for_getting_conf=tc-get-service-configuration
    :param service_name:
    :return:
    """
    if not service_name:
        raise Exception("You must specify a service_name value either as ENV variable or parameter")
    topic_for_getting_conf = os.environ.get('topic_for_getting_conf', 'tc-get-service-configuration')
    topic_for_setting_conf = os.environ.get('topic_for_setting_conf', 'tc-set-service-configuration')
    topic_for_setting_conf_no_avro = os.environ.get('topic_for_setting_conf_no_avro', 0)
    topic_for_getting_conf_no_avro = os.environ.get('topic_for_getting_conf_no_avro', 0)
    topic_for_monitoring_communication = os.environ.get('monitoring_communication_topic',
                                                        'services-configuration-monitoring')
    brokers_configuration = {
        'service_name': service_name,
        'brokers_uri': os.environ.get('brokers'),
        'schema_registry_url': os.environ.get('schema_registry'),
        'security_protocol': os.environ.get('security_protocol'),
        'ssl_ca_location': os.environ.get('ssl_ca_location'),
        'ssl_certificate_location': os.environ.get('ssl_certificate_location'),
        'ssl_key_location': os.environ.get('ssl_key_location'),
        'basic_auth_credentials_source': os.environ.get('basic_auth_credentials_source'),
        'sasl_mechanisms': os.environ.get('sasl_mechanisms'),
        'debug': os.environ.get('debug'),
        'api_version_request': os.environ.get('api_version_request', 1)

    }

    service_name = brokers_configuration.get('service_name')
    brokers_configuration.pop('service_name')
    if topic_for_getting_conf_no_avro:
        brokers_configuration.pop('schema_registry_url', '')
    monitoring_producer_instance = Producer(brokers_configuration=brokers_configuration,
                                            topic=topic_for_monitoring_communication)
    service_conf_requester_instance = Producer(brokers_configuration=brokers_configuration,
                                               topic=topic_for_getting_conf)

    brokers_configuration['group_id'] = os.environ.get('group_id', 'conf_requester_' + uuid.uuid4().hex)

    __start_consumer_and_producer_and_wait_until_service_conf_is_received(brokers_configuration=brokers_configuration,
                                                                          service_conf_requester_instance=service_conf_requester_instance,
                                                                          service_name=service_name,
                                                                          topic_for_setting_conf=topic_for_setting_conf,
                                                                          monitoring_producer_instance=monitoring_producer_instance)

    return listen_service_configuration()


def listen_service_configuration(service_name=os.environ.get('service_name')):
    """
    topic_for_setting_conf=tc-set-service-configuration
    topic_for_getting_conf=tc-get-service-configuration
    :param service_name:
    :return:
    """
    if not service_name:
        raise Exception("You must specify a service_name value either as ENV variable or parameter")
    topic_for_getting_conf = os.environ.get('topic_for_getting_conf', 'tc-get-service-configuration')
    topic_for_setting_conf = os.environ.get('topic_for_setting_conf', 'tc-set-service-configuration')
    topic_for_setting_conf_no_avro = os.environ.get('topic_for_setting_conf_no_avro', 0)
    topic_for_getting_conf_no_avro = os.environ.get('topic_for_getting_conf_no_avro', 0)
    topic_for_monitoring_communication = os.environ.get('monitoring_communication_topic',
                                                        'services-configuration-monitoring')
    brokers_configuration = {
        'service_name': service_name,
        'brokers_uri': os.environ.get('brokers'),
        'schema_registry_url': os.environ.get('schema_registry'),
        'security_protocol': os.environ.get('security_protocol'),
        'ssl_ca_location': os.environ.get('ssl_ca_location'),
        'ssl_certificate_location': os.environ.get('ssl_certificate_location'),
        'ssl_key_location': os.environ.get('ssl_key_location'),
        'basic_auth_credentials_source': os.environ.get('basic_auth_credentials_source'),
        'sasl_mechanisms': os.environ.get('sasl_mechanisms'),
        'debug': os.environ.get('debug'),
        'api_version_request': os.environ.get('api_version_request', 1)

    }

    service_name = brokers_configuration.get('service_name')
    brokers_configuration.pop('service_name')
    if topic_for_getting_conf_no_avro:
        brokers_configuration.pop('schema_registry_url', '')
    monitoring_producer_instance = Producer(brokers_configuration=brokers_configuration,
                                            topic=topic_for_monitoring_communication)
    service_conf_requester_instance = Producer(brokers_configuration=brokers_configuration,
                                               topic=topic_for_getting_conf)

    brokers_configuration['group_id'] = os.environ.get('group_id', 'conf_requester_' + uuid.uuid4().hex)

    __start_consumer_to_listen_to_future_updates_for_service_configuration(brokers_configuration=brokers_configuration,
                                                                           service_conf_requester_instance=service_conf_requester_instance,
                                                                           service_name=service_name,
                                                                           topic_for_setting_conf=topic_for_setting_conf,
                                                                           monitoring_producer_instance=monitoring_producer_instance)


def __init_consumer(brokers_configuration,
                    service_conf_requester_instance,
                    service_name,
                    topic_for_setting_conf, monitoring_producer_instance, just_listen=0):
    from service_configuration_controller.communication.consumers import ConfigurationConsumer

    consumer = ConfigurationConsumer(
        service_conf_requester_instance=service_conf_requester_instance,
        configuration_from_env=brokers_configuration,
        service_name=service_name,
        group_id=brokers_configuration.get('group_id'), offset=brokers_configuration.get('offset', 'latest'),
        topic=[topic_for_setting_conf],
        monitoring_producer_instance=monitoring_producer_instance,
        just_listen=just_listen)

    return consumer


def __start_consumer_to_listen_to_future_updates_for_service_configuration(brokers_configuration,
                                                                           service_conf_requester_instance,
                                                                           service_name,
                                                                           topic_for_setting_conf,
                                                                           monitoring_producer_instance, just_listen=0):
    """

    Here a consumer is started just listen to the given topic_for_setting_conf and update the configuration if new message will arrive.
    There will no outgoing messages to request the service configuration.
    The Thread is not-blocking and the control will be returned to the caller.

    :param brokers_configuration:
    :param service_conf_requester_instance:
    :param service_name:
    :param topic_for_setting_conf:
    :return:
    """

    consumerb = __init_consumer(brokers_configuration,
                                service_conf_requester_instance,
                                service_name,
                                topic_for_setting_conf, monitoring_producer_instance, just_listen=1)
    consumerb_th = threading.Thread(target=consumerb.run)
    consumerb_th.start()


def __start_consumer_and_producer_and_wait_until_service_conf_is_received(brokers_configuration,
                                                                          service_conf_requester_instance, service_name,
                                                                          topic_for_setting_conf,
                                                                          monitoring_producer_instance):
    """
    This method
    :param brokers_configuration:
    :param service_conf_requester_instance:
    :param service_name:
    :param topic_for_setting_conf:
    :return:
    """

    consumer = __init_consumer(brokers_configuration,
                               service_conf_requester_instance,
                               service_name,
                               topic_for_setting_conf, monitoring_producer_instance)
    consumer_th = threading.Thread(target=consumer.run)
    consumer_th.start()
    consumer_th.join()
