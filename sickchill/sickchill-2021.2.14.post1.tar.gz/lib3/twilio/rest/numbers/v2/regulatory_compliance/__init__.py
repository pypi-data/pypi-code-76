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
from twilio.rest.numbers.v2.regulatory_compliance.bundle import BundleList
from twilio.rest.numbers.v2.regulatory_compliance.end_user import EndUserList
from twilio.rest.numbers.v2.regulatory_compliance.end_user_type import EndUserTypeList
from twilio.rest.numbers.v2.regulatory_compliance.regulation import RegulationList
from twilio.rest.numbers.v2.regulatory_compliance.supporting_document import SupportingDocumentList
from twilio.rest.numbers.v2.regulatory_compliance.supporting_document_type import SupportingDocumentTypeList


class RegulatoryComplianceList(ListResource):

    def __init__(self, version):
        """
        Initialize the RegulatoryComplianceList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryComplianceList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryComplianceList
        """
        super(RegulatoryComplianceList, self).__init__(version)

        # Path Solution
        self._solution = {}

        # Components
        self._bundles = None
        self._end_users = None
        self._end_user_types = None
        self._regulations = None
        self._supporting_documents = None
        self._supporting_document_types = None

    @property
    def bundles(self):
        """
        Access the bundles

        :returns: twilio.rest.numbers.v2.regulatory_compliance.bundle.BundleList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.bundle.BundleList
        """
        if self._bundles is None:
            self._bundles = BundleList(self._version, )
        return self._bundles

    @property
    def end_users(self):
        """
        Access the end_users

        :returns: twilio.rest.numbers.v2.regulatory_compliance.end_user.EndUserList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.end_user.EndUserList
        """
        if self._end_users is None:
            self._end_users = EndUserList(self._version, )
        return self._end_users

    @property
    def end_user_types(self):
        """
        Access the end_user_types

        :returns: twilio.rest.numbers.v2.regulatory_compliance.end_user_type.EndUserTypeList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.end_user_type.EndUserTypeList
        """
        if self._end_user_types is None:
            self._end_user_types = EndUserTypeList(self._version, )
        return self._end_user_types

    @property
    def regulations(self):
        """
        Access the regulations

        :returns: twilio.rest.numbers.v2.regulatory_compliance.regulation.RegulationList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.regulation.RegulationList
        """
        if self._regulations is None:
            self._regulations = RegulationList(self._version, )
        return self._regulations

    @property
    def supporting_documents(self):
        """
        Access the supporting_documents

        :returns: twilio.rest.numbers.v2.regulatory_compliance.supporting_document.SupportingDocumentList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.supporting_document.SupportingDocumentList
        """
        if self._supporting_documents is None:
            self._supporting_documents = SupportingDocumentList(self._version, )
        return self._supporting_documents

    @property
    def supporting_document_types(self):
        """
        Access the supporting_document_types

        :returns: twilio.rest.numbers.v2.regulatory_compliance.supporting_document_type.SupportingDocumentTypeList
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.supporting_document_type.SupportingDocumentTypeList
        """
        if self._supporting_document_types is None:
            self._supporting_document_types = SupportingDocumentTypeList(self._version, )
        return self._supporting_document_types

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Numbers.V2.RegulatoryComplianceList>'


class RegulatoryCompliancePage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the RegulatoryCompliancePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryCompliancePage
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryCompliancePage
        """
        super(RegulatoryCompliancePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of RegulatoryComplianceInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryComplianceInstance
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryComplianceInstance
        """
        return RegulatoryComplianceInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Numbers.V2.RegulatoryCompliancePage>'


class RegulatoryComplianceInstance(InstanceResource):

    def __init__(self, version, payload):
        """
        Initialize the RegulatoryComplianceInstance

        :returns: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryComplianceInstance
        :rtype: twilio.rest.numbers.v2.regulatory_compliance.RegulatoryComplianceInstance
        """
        super(RegulatoryComplianceInstance, self).__init__(version)

        # Context
        self._context = None
        self._solution = {}

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Numbers.V2.RegulatoryComplianceInstance>'
