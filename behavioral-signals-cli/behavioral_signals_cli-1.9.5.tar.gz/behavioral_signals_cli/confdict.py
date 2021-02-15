#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
#

import os
import logging

from . import utils
from .utils import die

#
# the main goal of this module is to merge cli options that come from
# different sources, with a specific priority as follows:
#
# internal defaults
# environment variables
# configuration (file)
# command line options
#
# the configuration file is simply a yml file with structure:
# sections:
#   sectionname:
#      ... (rest of the configuration)
#
# the configuration can be specified as
# a constant (dict) [confDict]
# a specific pathname [configFile] -- commandline
# a list of pathnames [configs]
#
# searched in this order
# the specified 'tag' selects a configuration within the configuration file
# (honoring sectionName, if specified)

# The the location of config, the sectionname, and the tag
# may be specified in the command line, but this is done before merge is called
# It will no overwrite earlier in the order values by nulls though

# -- internalDict : internal defaults
# -- envDict      : settings through environment variables
# -- cliDict      : settings from the command line
# -- confDict     : configuration dict

# -- the next three options will be used only if confDict is None
# -- configFile   : a specific config file (error if not found)
# -- configs      : list of configuration files (ok if not found)

# -- tag          : named section inside config to use in merging
# -- sectionName  : name of the top level element of the config dict

# -- returns a new dict, the result of merge of optDict and config dict

def merge(internalDict={}, envDict={}, cliDict={}, confDict=None,
          configFile=None, tag="default", sectionsName="sections", configs=[]):

    def getConfDict(confDict, configFile, configs):
        # -- at first, we need to deal with the (external) configuration
        if confDict is not None:
            return confDict, "inline"

        if configFile is not None:
            path = configFile
            if not os.path.exists(path):
                die("{}: configuration file does not exist".format(path))
        else:
            # -- if no configuration is specified, look for one in configs
            path = None
            for f in configs:
                fp = os.path.expanduser(f)
                if os.path.exists(fp):
                    path = fp
                    break
            if path is None:
                logging.info("no configuration found in {}".format(configs))
                return None, ""

        logging.info("configuration: using {}".format(path))
        return utils.readConf(path), path

    # -- locate the correct section in the configuration dict
    def getTaggedConf(cdict, sectionsName, tag):
        if cdict is None:
            return {}
        # -- the config dict is supposed to contain "sections"
        if sectionsName is None:
            sectionDict = cdict
        else:
            sectionDict = cdict[sectionsName]
        if tag not in list(sectionDict.keys()):
            die("{}: tag not found in configuration".format(tag))
        cdict = sectionDict[tag]

        # -- in the event the configuration section is empty ...
        if cdict is None:
            cdict = {}
        return cdict

    cdict1, location = getConfDict(confDict, configFile, configs)
    cdict = getTaggedConf(cdict1, sectionsName, tag)
    res = mergeDicts([internalDict, envDict, cdict, cliDict])
    res['configLocation'] = location
    return res

#
# merge list of dictionaries, later dict values survive the earlier ones
#


def mergeDicts(dictList, nulls=[None, '']):
    # dictList is an ordered list of dicts. The last dict has
    # the highest priority.

    res = {}
    for adict in dictList:
        for key in list(adict.keys()):
            # -- establish a default value, if not set before
            if key not in list(res.keys()):
                res[key] = adict[key]
            # -- refuse to overwrite with a 'null' value (in nulls)
            if adict[key] not in nulls:
                res[key] = adict[key]
    return res


if __name__ == "__main__":
    internalDict = {'ivar': 1, 'a': 'internal'}

    envDict = {'evar': 2, 'b': 'env'}

    cliDict = {'a': 'cli-a', 'b': 'cli-b', 'c': 'cli-c'}

    confDict = {
        'sections': {
            'default': {'a': 'conf-a', 'b': 'conf-b', 'c': None}
        }
    }

    mdict = merge(
        internalDict=internalDict,
        envDict=envDict,
        confDict=confDict,
        cliDict=cliDict)
    utils.ppr(mdict)
