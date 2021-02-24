# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pathlib as pt
import logging as log

from fameio.source.AttributeValidator import AttributeValidator, AttributeType
from fameio.source.TimeSeriesManager import TimeSeriesManager
from fameio.source.tools import arg_handling_make_config, get_valid_key, log_and_raise, set_up_logger
from fameio.source.loader import load_yaml
from fameio.source.FameTime import FameTime
from fameprotobuf import InputFile_pb2
from fameprotobuf import Contract_pb2


DEFAULT_CONFIG = {"log_level": "warning",
                  "output_file": "config.pb",
                  "log_file": None,
                  }


def set_general_properties(properties, proto):
    """Set the general properties in the given protobuf"""
    valid_keys = [field.name for field in InputFile_pb2._INPUTDATA.fields]
    for property_name, property_value in properties.items():
        property_name = get_valid_key(property_name, valid_keys)
        if not hasattr(property_value, "keys"):
            setattr(proto, property_name, property_value)
        else:
            parent = getattr(proto, property_name)
            valid_child_keys = parent.DESCRIPTOR.fields_by_name.keys()
            for child_property_name, child_property_value in property_value.items():
                child_property_name = get_valid_key(child_property_name, valid_child_keys)
                child_property_value = convert_string_if_is_datetime(child_property_value)
                setattr(parent, child_property_name, child_property_value)
        log.info("Set general properties for `{}`".format(property_name))


def convert_string_if_is_datetime(value):
    """Returns given `value` in FameTime steps if it is DateTime string, otherwise returns `value`"""
    if FameTime.is_datetime(value):
        value = int(FameTime.convert_datetime_to_fame_time_step(value))
    return value


def set_attributes(pb_agent, attributes, time_series_manager, validator):
    """Adds all attributes in the given list to the given agent proto buffer"""
    if attributes is not None:
        agent_type = pb_agent.className
        for attribute_name, attribute_value in attributes.items():
            pb_field = pb_agent.field.add()
            pb_field.fieldName = attribute_name
            attribute_type = validator.get_attribute_type(agent_type, attribute_name)
            if validator.is_valid(agent_type, attribute_name, attribute_value):
                if attribute_type is AttributeType.INTEGER:
                    pb_field.intValue = attribute_value
                elif attribute_type is AttributeType.DOUBLE:
                    pb_field.doubleValue.extend([attribute_value])
                elif attribute_type is AttributeType.ENUM:
                    pb_field.stringValue = attribute_value
                elif attribute_type is AttributeType.TIME_SERIES:
                    if isinstance(attribute_value, str):
                        file_name = pt.Path(attribute_value).as_posix()
                        pb_field.seriesId = time_series_manager.save_get_time_series_id(file_name)
                    else:
                        pb_field.seriesId = time_series_manager.save_get_time_series_id(attribute_value)
                elif attribute_type is AttributeType.DOUBLE_LIST:
                    for element in attribute_value:
                        pb_field.doubleValue.extend([element])
                else:
                    log_and_raise("AttributeType '{}' not implemented.".format(attribute_type))
            else:
                log_and_raise("'{}' not allowed in attribute '{}' of agent {}".format(attribute_value, attribute_name, pb_agent.id))


def get_or_error(agent, param):
    """Gets given `param` from dictionary or raises error if field is missing"""
    try:
        return agent[param]
    except KeyError:
        log_and_raise("Cannot find '{}' in `agent` {}".format(param, agent))


def set_agents_and_time_series(agent_list, proto_buffer, validator):
    """
    Iterates through all agents, adds them and all of their attributes to the given proto buffer and also
    adds all referenced files as time series to the proto_buffer. Ensures proper attribute parameterization and format.
    """
    time_series_manager = TimeSeriesManager()
    for agent in agent_list:
        agent = convert_keys_to_lower(agent)
        pb_agent = proto_buffer.agent.add()
        pb_agent.className = get_or_error(agent, "type")
        pb_agent.id = get_or_error(agent, "id")
        if "attributes" in agent:
            attributes = agent.get("attributes")
            set_attributes(pb_agent, attributes, time_series_manager, validator)
        log.info("Set `Attributes` for agent `{}` with ID `{}`".format(pb_agent.className, pb_agent.id))
    time_series_manager.add_time_series_to_proto_buffer(proto_buffer)


def convert_keys_to_lower(agent):
    """Returns given dictionary with `keys` in lower case"""
    return {keys.lower(): value for keys, value in agent.items()}


def set_contracts(contracts, proto_buffer):
    """Adds all contracts in the given list to the given proto buffer"""
    valid_keys = [field.name for field in Contract_pb2._PROTOCONTRACT.fields]
    for contract in contracts:
        pb_contract = proto_buffer.contract.add()
        for key, value in contract.items():
            key = get_valid_key(key, valid_keys)
            value = convert_string_if_is_datetime(value)
            setattr(pb_contract, key, value)
    log.info("Added contracts to protobuf file.")


def write_protobuf_to_disk(output_file, proto_input_data):
    """Writes given `protobuf_input_data` in `output_file` to disk"""
    f = open(output_file, "wb")
    f.write(proto_input_data.SerializeToString())
    f.close()
    log.info("Saved protobuf file `{}` to disk".format(output_file))


def run(file, config=DEFAULT_CONFIG):
    """Executes the main workflow for the building of a FAME configuration file"""
    set_up_logger(level=config["log_level"], file_name=config["log_file"])

    config_data = load_yaml(file)
    validator = AttributeValidator(config_data["Schema"])
    proto_input_data = InputFile_pb2.InputData()
    set_general_properties(config_data["GeneralProperties"], proto_input_data)
    set_agents_and_time_series(config_data["Agents"], proto_input_data, validator)

    contract_list = config_data["Contracts"]
    set_contracts(contract_list, proto_input_data)

    write_protobuf_to_disk(config["output_file"], proto_input_data)

    log.info("Completed conversion of all input in `{}` to protobuf file `{}`".format(file, config["output_file"]))


if __name__ == '__main__':
    input_file, run_config = arg_handling_make_config(DEFAULT_CONFIG)
    run(input_file, run_config)
