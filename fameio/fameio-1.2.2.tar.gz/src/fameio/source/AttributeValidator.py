# !/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum
import logging as log

from .tools import log_and_raise


class AttributeValidator:
    """ Handles validation of agent `Attributes` in scenario YAML files based on given `schema`"""
    type_schema = dict()

    def __init__(self, schema):
        """Load rules for given Schema"""
        for agent, agent_details in schema['AgentTypes'].items():
            if agent_details is None:
                log.info("Schema for '{}' is empty. Please make sure to provide valid `Inputs` and/or `Products` in "
                         "order to ensure a correct validation.".format(agent))
            else:
                if 'Attributes' in agent_details:
                    self.type_schema[agent] = agent_details['Attributes']
                else:
                    log.info("Agent '{}' has no specified 'Attributes'.".format(agent))

    def get_attribute_type(self, agent_type, attribute_name):
        """ Returns AttributeType of given `attribute_name` of `agent_type` as specified in scenario schema """
        try:
            agent = self.type_schema[agent_type]
        except KeyError:
            log_and_raise("Schema has no agent '{}'.".format(agent_type))

        try:
            attribute = agent[attribute_name]
        except KeyError:
            log_and_raise("Schema agent '{}' has no attribute '{}'.".format(agent_type, attribute_name))

        try:
            attribute_type = attribute['AttributeType']
        except KeyError:
            log_and_raise("'AttributeType' missing in agent '{}' attribute '{}'.".format(agent_type, attribute_name))

        try:
            return AttributeType[attribute_type.upper()]
        except KeyError:
            log_and_raise("AttributeType '{}' not implemented.".format(attribute_type.upper()))

    def is_valid(self, agent_type, attribute_name, value):
        """ Returns true if `value` can be matched to `data_type` of given `attribute_name`"""
        data_type = self.get_attribute_type(agent_type, attribute_name)
        return AttributeValidator.is_compatible(data_type, value) and \
               AttributeValidator.allowed_value(self.type_schema[agent_type][attribute_name], value)

    @staticmethod
    def is_compatible(data_type, value):
        """ Returns true if attribute type of given `value` is compatible to required `attribute_type`. """
        if data_type is AttributeType.INTEGER:
            return isinstance(value, int)
        elif data_type is AttributeType.DOUBLE:
            return isinstance(value, (int, float))
        elif data_type is AttributeType.DOUBLE_LIST:
            return all(isinstance(x, (int, float)) for x in value)
        elif data_type is AttributeType.ENUM:
            return isinstance(value, str)
        elif data_type is AttributeType.TIME_SERIES:
            return isinstance(value, (str, int, float))
        else:
            log_and_raise("Validation not implemented for AttributeType '{}'.".format(data_type))

    @staticmethod
    def allowed_value(attribute_definition, value):
        """
        Returns true if `value` matches one allowed 'Values' of `attribute_definition` or true,
        if no 'Values'-restrictions are specified.
        """
        if 'Values' in attribute_definition:
            return value in attribute_definition['Values']
        return True


class AttributeType(Enum):
    INTEGER = 0
    DOUBLE = 1
    ENUM = 2
    TIME_SERIES = 3
    DOUBLE_LIST = 4
