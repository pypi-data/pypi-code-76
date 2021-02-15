# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class ExportConfigurationList(ListResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version):
        """
        Initialize the ExportConfigurationList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationList
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationList
        """
        super(ExportConfigurationList, self).__init__(version)

        # Path Solution
        self._solution = {}

    def get(self, resource_type):
        """
        Constructs a ExportConfigurationContext

        :param resource_type: The type of communication – Messages, Calls

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        """
        return ExportConfigurationContext(self._version, resource_type=resource_type, )

    def __call__(self, resource_type):
        """
        Constructs a ExportConfigurationContext

        :param resource_type: The type of communication – Messages, Calls

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        """
        return ExportConfigurationContext(self._version, resource_type=resource_type, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.BulkExports.ExportConfigurationList>'


class ExportConfigurationPage(Page):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, response, solution):
        """
        Initialize the ExportConfigurationPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationPage
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationPage
        """
        super(ExportConfigurationPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ExportConfigurationInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        """
        return ExportConfigurationInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.BulkExports.ExportConfigurationPage>'


class ExportConfigurationContext(InstanceContext):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, resource_type):
        """
        Initialize the ExportConfigurationContext

        :param Version version: Version that contains the resource
        :param resource_type: The type of communication – Messages, Calls

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        """
        super(ExportConfigurationContext, self).__init__(version)

        # Path Solution
        self._solution = {'resource_type': resource_type, }
        self._uri = '/Exports/{resource_type}/Configuration'.format(**self._solution)

    def fetch(self):
        """
        Fetch the ExportConfigurationInstance

        :returns: The fetched ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return ExportConfigurationInstance(
            self._version,
            payload,
            resource_type=self._solution['resource_type'],
        )

    def update(self, enabled=values.unset, webhook_url=values.unset,
               webhook_method=values.unset):
        """
        Update the ExportConfigurationInstance

        :param bool enabled: Whether files are automatically generated
        :param unicode webhook_url: URL targeted at export
        :param unicode webhook_method: Whether to GET or POST to the webhook url

        :returns: The updated ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        """
        data = values.of({'Enabled': enabled, 'WebhookUrl': webhook_url, 'WebhookMethod': webhook_method, })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return ExportConfigurationInstance(
            self._version,
            payload,
            resource_type=self._solution['resource_type'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.BulkExports.ExportConfigurationContext {}>'.format(context)


class ExportConfigurationInstance(InstanceResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, payload, resource_type=None):
        """
        Initialize the ExportConfigurationInstance

        :returns: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        """
        super(ExportConfigurationInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'enabled': payload.get('enabled'),
            'webhook_url': payload.get('webhook_url'),
            'webhook_method': payload.get('webhook_method'),
            'resource_type': payload.get('resource_type'),
            'url': payload.get('url'),
        }

        # Context
        self._context = None
        self._solution = {'resource_type': resource_type or self._properties['resource_type'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: ExportConfigurationContext for this ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationContext
        """
        if self._context is None:
            self._context = ExportConfigurationContext(
                self._version,
                resource_type=self._solution['resource_type'],
            )
        return self._context

    @property
    def enabled(self):
        """
        :returns: Whether files are automatically generated
        :rtype: bool
        """
        return self._properties['enabled']

    @property
    def webhook_url(self):
        """
        :returns: URL targeted at export
        :rtype: unicode
        """
        return self._properties['webhook_url']

    @property
    def webhook_method(self):
        """
        :returns: Whether to GET or POST to the webhook url
        :rtype: unicode
        """
        return self._properties['webhook_method']

    @property
    def resource_type(self):
        """
        :returns: The type of communication – Messages, Calls
        :rtype: unicode
        """
        return self._properties['resource_type']

    @property
    def url(self):
        """
        :returns: The URL of this resource.
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self):
        """
        Fetch the ExportConfigurationInstance

        :returns: The fetched ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        """
        return self._proxy.fetch()

    def update(self, enabled=values.unset, webhook_url=values.unset,
               webhook_method=values.unset):
        """
        Update the ExportConfigurationInstance

        :param bool enabled: Whether files are automatically generated
        :param unicode webhook_url: URL targeted at export
        :param unicode webhook_method: Whether to GET or POST to the webhook url

        :returns: The updated ExportConfigurationInstance
        :rtype: twilio.rest.preview.bulk_exports.export_configuration.ExportConfigurationInstance
        """
        return self._proxy.update(enabled=enabled, webhook_url=webhook_url, webhook_method=webhook_method, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.BulkExports.ExportConfigurationInstance {}>'.format(context)
