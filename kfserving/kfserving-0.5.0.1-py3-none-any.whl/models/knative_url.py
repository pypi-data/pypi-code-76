# Copyright 2020 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    KFServing

    Python SDK for KFServing  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kfserving.configuration import Configuration


class KnativeURL(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'force_query': 'bool',
        'fragment': 'str',
        'host': 'str',
        'opaque': 'str',
        'path': 'str',
        'raw_path': 'str',
        'raw_query': 'str',
        'scheme': 'str',
        'user': 'NetUrlUserinfo'
    }

    attribute_map = {
        'force_query': 'ForceQuery',
        'fragment': 'Fragment',
        'host': 'Host',
        'opaque': 'Opaque',
        'path': 'Path',
        'raw_path': 'RawPath',
        'raw_query': 'RawQuery',
        'scheme': 'Scheme',
        'user': 'User'
    }

    def __init__(self, force_query=None, fragment=None, host=None, opaque=None, path=None, raw_path=None, raw_query=None, scheme=None, user=None, local_vars_configuration=None):  # noqa: E501
        """KnativeURL - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._force_query = None
        self._fragment = None
        self._host = None
        self._opaque = None
        self._path = None
        self._raw_path = None
        self._raw_query = None
        self._scheme = None
        self._user = None
        self.discriminator = None

        self.force_query = force_query
        self.fragment = fragment
        self.host = host
        self.opaque = opaque
        self.path = path
        self.raw_path = raw_path
        self.raw_query = raw_query
        self.scheme = scheme
        self.user = user

    @property
    def force_query(self):
        """Gets the force_query of this KnativeURL.  # noqa: E501

        encoded path hint (see EscapedPath method)  # noqa: E501

        :return: The force_query of this KnativeURL.  # noqa: E501
        :rtype: bool
        """
        return self._force_query

    @force_query.setter
    def force_query(self, force_query):
        """Sets the force_query of this KnativeURL.

        encoded path hint (see EscapedPath method)  # noqa: E501

        :param force_query: The force_query of this KnativeURL.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and force_query is None:  # noqa: E501
            raise ValueError("Invalid value for `force_query`, must not be `None`")  # noqa: E501

        self._force_query = force_query

    @property
    def fragment(self):
        """Gets the fragment of this KnativeURL.  # noqa: E501

        encoded query values, without '?'  # noqa: E501

        :return: The fragment of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._fragment

    @fragment.setter
    def fragment(self, fragment):
        """Sets the fragment of this KnativeURL.

        encoded query values, without '?'  # noqa: E501

        :param fragment: The fragment of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and fragment is None:  # noqa: E501
            raise ValueError("Invalid value for `fragment`, must not be `None`")  # noqa: E501

        self._fragment = fragment

    @property
    def host(self):
        """Gets the host of this KnativeURL.  # noqa: E501

        username and password information  # noqa: E501

        :return: The host of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this KnativeURL.

        username and password information  # noqa: E501

        :param host: The host of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and host is None:  # noqa: E501
            raise ValueError("Invalid value for `host`, must not be `None`")  # noqa: E501

        self._host = host

    @property
    def opaque(self):
        """Gets the opaque of this KnativeURL.  # noqa: E501


        :return: The opaque of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._opaque

    @opaque.setter
    def opaque(self, opaque):
        """Sets the opaque of this KnativeURL.


        :param opaque: The opaque of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and opaque is None:  # noqa: E501
            raise ValueError("Invalid value for `opaque`, must not be `None`")  # noqa: E501

        self._opaque = opaque

    @property
    def path(self):
        """Gets the path of this KnativeURL.  # noqa: E501

        host or host:port  # noqa: E501

        :return: The path of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this KnativeURL.

        host or host:port  # noqa: E501

        :param path: The path of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and path is None:  # noqa: E501
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def raw_path(self):
        """Gets the raw_path of this KnativeURL.  # noqa: E501

        path (relative paths may omit leading slash)  # noqa: E501

        :return: The raw_path of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._raw_path

    @raw_path.setter
    def raw_path(self, raw_path):
        """Sets the raw_path of this KnativeURL.

        path (relative paths may omit leading slash)  # noqa: E501

        :param raw_path: The raw_path of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and raw_path is None:  # noqa: E501
            raise ValueError("Invalid value for `raw_path`, must not be `None`")  # noqa: E501

        self._raw_path = raw_path

    @property
    def raw_query(self):
        """Gets the raw_query of this KnativeURL.  # noqa: E501

        append a query ('?') even if RawQuery is empty  # noqa: E501

        :return: The raw_query of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._raw_query

    @raw_query.setter
    def raw_query(self, raw_query):
        """Sets the raw_query of this KnativeURL.

        append a query ('?') even if RawQuery is empty  # noqa: E501

        :param raw_query: The raw_query of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and raw_query is None:  # noqa: E501
            raise ValueError("Invalid value for `raw_query`, must not be `None`")  # noqa: E501

        self._raw_query = raw_query

    @property
    def scheme(self):
        """Gets the scheme of this KnativeURL.  # noqa: E501


        :return: The scheme of this KnativeURL.  # noqa: E501
        :rtype: str
        """
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        """Sets the scheme of this KnativeURL.


        :param scheme: The scheme of this KnativeURL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and scheme is None:  # noqa: E501
            raise ValueError("Invalid value for `scheme`, must not be `None`")  # noqa: E501

        self._scheme = scheme

    @property
    def user(self):
        """Gets the user of this KnativeURL.  # noqa: E501


        :return: The user of this KnativeURL.  # noqa: E501
        :rtype: NetUrlUserinfo
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this KnativeURL.


        :param user: The user of this KnativeURL.  # noqa: E501
        :type: NetUrlUserinfo
        """
        if self.local_vars_configuration.client_side_validation and user is None:  # noqa: E501
            raise ValueError("Invalid value for `user`, must not be `None`")  # noqa: E501

        self._user = user

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, KnativeURL):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, KnativeURL):
            return True

        return self.to_dict() != other.to_dict()
