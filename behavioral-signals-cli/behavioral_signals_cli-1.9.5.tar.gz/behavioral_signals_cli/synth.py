#
# generate synthetic metadata
#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
import csv
import sys
import yaml
import os
import random
import pprint
import json


class SynthMeta():
    def __init__(self, configFile="post.yml"):
        if not os.path.exists(configFile):
            sys.exit("{}: does not exist".format(configFile))

        self.pp = pprint.PrettyPrinter(indent=2)
        self.confDict = self.readConf(configFile)

    def generate(self, args, output="/dev/stdout"):
        """
        Generate a csv line using the rules for each arg supplied
        """
        fp = open(output, "w")
        cf = csv.writer(fp, delimiter=',')
        for file in args:
            line = self.generateLine(file)
            cf.writerow(line)

    def readConf(self, cfile):
        """
        Read the yml config file
        """
        if not os.path.exists(cfile):
            sys.exit("{}: does not exist".format(cfile))
        with open(cfile, "r") as f:
            return yaml.safe_load(f)

    def generateLine(self, filename):
        """
        Generate a line using random choices from supplied variables
        """
        ldict = {
            'filename': filename,
            'json': {}
        }

        d = {}
        metaAttribute = None

        for key, value in self.confDict['fields'].items():
            # make a note of the json attribute
            if value == "{json}":
                metaAttribute = key
                continue
            # pick a random choice from a list
            if type(value) == list:
                d[key] = random.choice(value)
                continue
            # assign this attribute from the dictionary
            if type(value) == str:
                if "{" in value:
                    d[key] = value.format(**ldict)
                    continue
            # constant
            d[key] = value

        # form the meta dict
        metaDict = {}
        for attr in self.confDict['json_attributes']:
            metaDict[attr] = d[attr]

        serviceRec = []
        # find the attribute that holds the json payload, if any
        for attr in self.confDict['csv_attributes']:
            if attr == metaAttribute:
                serviceRec += [json.dumps(metaDict)]
            else:
                serviceRec += [d[attr]]

        return serviceRec


def main():
    """
    The generated bsi-meta uses this one
    """
    syn = SynthMeta(configFile="post.yml")
    if len(sys.argv) == 1:
        sys.exit("usage: bsi-meta [audio-files]")

    syn.generate(sys.argv[1:])
