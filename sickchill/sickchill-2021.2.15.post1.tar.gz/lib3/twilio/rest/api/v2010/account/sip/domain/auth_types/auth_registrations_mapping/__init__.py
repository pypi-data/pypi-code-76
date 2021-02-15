# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.auth_registrations_credential_list_mapping import AuthRegistrationsCredentialListMappingList


class AuthTypeRegistrationsList(ListResource):

    def __init__(self, version, account_sid, domain_sid):
        """
        Initialize the AuthTypeRegistrationsList

        :param Version version: Version that contains the resource
        :param account_sid: The SID of the Account that created the resource
        :param domain_sid: The unique string that identifies the resource

        :returns: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsList
        :rtype: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsList
        """
        super(AuthTypeRegistrationsList, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, 'domain_sid': domain_sid, }

        # Components
        self._credential_list_mappings = None

    @property
    def credential_list_mappings(self):
        """
        Access the credential_list_mappings

        :returns: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.auth_registrations_credential_list_mapping.AuthRegistrationsCredentialListMappingList
        :rtype: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.auth_registrations_credential_list_mapping.AuthRegistrationsCredentialListMappingList
        """
        if self._credential_list_mappings is None:
            self._credential_list_mappings = AuthRegistrationsCredentialListMappingList(
                self._version,
                account_sid=self._solution['account_sid'],
                domain_sid=self._solution['domain_sid'],
            )
        return self._credential_list_mappings

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AuthTypeRegistrationsList>'


class AuthTypeRegistrationsPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the AuthTypeRegistrationsPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The SID of the Account that created the resource
        :param domain_sid: The unique string that identifies the resource

        :returns: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsPage
        :rtype: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsPage
        """
        super(AuthTypeRegistrationsPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of AuthTypeRegistrationsInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsInstance
        """
        return AuthTypeRegistrationsInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            domain_sid=self._solution['domain_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AuthTypeRegistrationsPage>'


class AuthTypeRegistrationsInstance(InstanceResource):

    def __init__(self, version, payload, account_sid, domain_sid):
        """
        Initialize the AuthTypeRegistrationsInstance

        :returns: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.auth_types.auth_registrations_mapping.AuthTypeRegistrationsInstance
        """
        super(AuthTypeRegistrationsInstance, self).__init__(version)

        # Context
        self._context = None
        self._solution = {'account_sid': account_sid, 'domain_sid': domain_sid, }

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AuthTypeRegistrationsInstance>'
