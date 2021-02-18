# encoding: utf-8

u"""
============================================================
Changes the uri by modifying, removing or adding parameters
------------------------------------------------------------
Filter: string to match in uri e.g. google
Parameters: JSON dict of 'add', 'remove', 'modify', each
            one being a list of key value pairs.
            for remove, you can match a specific value or
            if the value is "", it'll remove all instances
            of that parameter.
            For modify, when there's only one instance of
            a parameter in the uri, just supply a single
            key:value pair. If there are multiple instances
            then te value needs to be another dictionary
            with 'old' and 'new' key value pairs.
------------------------------------------------------------
"""

import requests
import logging_helper
from pyhttpintercept.intercept.handlers.support import (decorate_uri_modifier_for_json_parameters,
                                                        decorate_uri_modifier_for_filter)
from urlparse import urlparse, urlunparse
logging = logging_helper.setup_logging()

ADD = 'add'
REMOVE = 'remove'
MODIFY = 'modify'

def extract_modification_list(modifier,
                              action):
    """
    Pulls a list of modifications associated to a particular action from the modifier
    parameters.
    Returns and empty list if there are none.
    If there's just one modification, puts that into a list before returning.

    :param modifier: modifier object
    :param action: key into the modifier parameters dictionary ('add', 'modify' or 'remove')
    :return: list of modifications
    """
    try:
        parameter_list = modifier.parameters['params'][action]
        if not isinstance(parameter_list, list):
            # single parameter, so put it into a list now
            # to make processing easier later
            parameter_list = [parameter_list]
    except KeyError:
        # action not provided, so return an empty list
        parameter_list = []
    return parameter_list


def remove_parameters(modifier,
                      params):

    removals = extract_modification_list(modifier=modifier,
                                         action=REMOVE)
    if not removals:
        return

    remove_indexes = []

    for i, (k, v) in enumerate(params):
        for removal in removals:
            for remove_key, remove_value in removal.items():
                if k == remove_key:
                    if v == remove_value or remove_value == "":
                        remove_indexes.append(i)

    for i in reversed(remove_indexes):
        params.pop(i)


def modify_parameters(modifier,
                      params):
    modifications = extract_modification_list(modifier=modifier,
                                              action=MODIFY)
    if not modifications:
        return

    for i, (k, v) in enumerate(params):
        for modification in modifications:
            for mod_key, mod_value in modification.items():
                if k == mod_key:
                    if isinstance(mod_value, dict):
                        match_value = mod_value['old']
                        new_value = mod_value['new']
                    else:
                        match_value = ""
                        new_value = mod_value
                    if v == match_value or match_value == "":
                        params[i][1] = new_value


def add_parameters(modifier,
                   params):
    additions = extract_modification_list(modifier=modifier,
                                          action=ADD)
    if not additions:
        return

    for addition in additions:
        for k, v in addition.items():
            params.append([k, v])


@decorate_uri_modifier_for_json_parameters
@decorate_uri_modifier_for_filter
def modify(uri,
           modifier):
    if modifier.filter in uri:
        parsed_uri = requests.utils.urlparse(uri)

        params = [param.split('=') for param in parsed_uri.query.split('&')]

        remove_parameters(modifier=modifier,
                          params=params)

        modify_parameters(modifier=modifier,
                          params=params)

        add_parameters(modifier=modifier,
                       params=params)

        params = u'&'.join([u"{k}={v}".format(k=k, v=v) for k, v in params if v])

        uri = urlunparse((parsed_uri.scheme,
                          parsed_uri.netloc,
                          parsed_uri.path,
                          parsed_uri.params,
                          params,
                          parsed_uri.fragment))
    return uri
