#!/usr/bin/env python3
#-*-coding:utf-8-*-

import argparse
import configparser
import csv
import datetime
import glob
import json
import os
import re
import time
from pathlib import Path
from pymongo import MongoClient


class Database(object):
    def __call__(self, database, debug):
        if database == "_":
            mongo_client = MongoClient("mongodb://fsr-ub1664-130.ea.freescale.net")
        elif database == "":
            mongo_client = MongoClient()
        else:
            mongo_client = MongoClient(database)

        db = mongo_client.benchmarking
        collection = db.measurements_test if debug else db.measurements
        return collection


class JsonLoader(object):
    def load(self, result):
        with open(result, 'r') as f:
            json_data = json.load(f)
        return json_data


class Csv1Loader(object):
    def __nested_set(self, dic, keys):
        for key in keys[:-2]:
            dic = dic.setdefault(key, {})
        dic["score"] = keys[-2]
        dic["metric"] = keys[-1]

    def load(self, result):
        json_data = {}
        with open(result, 'r') as f:
            data = csv.reader(f)
            last_line_length = 0
            for line in data:
                cur_line_length = len(line)
                if last_line_length != 0 and cur_line_length != last_line_length:
                    raise
                if line[0] == "":
                    raise
                last_line_length = cur_line_length
                self.__nested_set(json_data, line)
        return json_data


class Csv2Loader(object):
    def load(self, result):
        json_data = {}
        with open(result, 'r') as f:
            data = csv.reader(f)
            content = list(zip(*[row for row in data]))
            for item in content:
                m = re.findall(r"(.+)[(/](\w+)", item[0])
                if m:
                    name = m[0][0]
                    unit = m[0][1]
                    json_data.setdefault(name, {})
                    if unit == "V":
                        json_data[name]["Voltage"] = {
                            "metric": "V",
                            "raw_data": [float(i) for i in list(item[1:])]
                        }
                    elif unit == "A":
                        json_data[name]["Current"] = {
                            "metric": "A",
                            "raw_data": [float(i) for i in list(item[1:])]
                        }
                    elif unit == "mA":
                        json_data[name]["Current"] = {
                            "metric": "A",
                            "raw_data": [float(i)/1000 for i in list(item[1:])]
                        }
        return json_data


class Worker(object):
    class MyConfigParser(configparser.ConfigParser):
        def as_dict(self):
            d = dict(self._sections)
            for k in d:
                d[k] = dict(self._defaults, **d[k])
                d[k].pop('__name__', None)
            d[k] = {key: d[k][key].upper() for key in d[k]}
            return d

    def __init__(self, *args, **kwargs):
        self.config = kwargs["config"]
        self.result = kwargs["result"]
        self.debug = kwargs["debug"]

        self.cfg = {}
        self.rlt = {}

        self.loader_maps = {
            "LINUX#PERFORMANCE#_": Csv1Loader(),
            "LINUX#POWER#BCU": JsonLoader(),
            "LINUX#POWER#NOBCU": Csv2Loader(),
            "ANDROID#PERFORMANCE#_": JsonLoader(),
            "ANDROID#POWER#BCU": JsonLoader(),
            "ANDROID#POWER#NOBCU": Csv2Loader(),
        }

    def __parse_config(self):
        config = Worker.MyConfigParser()
        config.read(self.config)
        self.cfg = config.as_dict().get("release_info", {})

    def __parse_result(self):
        loader_key = "#".join((self.cfg.get("os", ""), self.cfg.get("type", ""), self.cfg.get("source", "_")))
        loader = self.loader_maps.get(loader_key, None)
        self.rlt = loader.load(self.result)

    def __submit(self):
        database = self.cfg.get("database", "_")
        reviewed = self.cfg.get("reviewed", "NO").upper()
        if reviewed != "YES":
            reviewed = "NO"

        db_result = self.cfg
        db_result["date"] = datetime.datetime.fromtimestamp(time.time(), None)
        db_result["reviewed"] = reviewed
        db_result["measurement_file"] = "N/A"
        db_result["note"] = "N/A"
        db_result["results"] = self.rlt
        db_result["workload"] = Path(self.result).stem

        collection = Database()(database, self.debug)
        collection.insert_one(db_result)

    def run(self):
        self.__parse_config()
        self.__parse_result()
        self.__submit()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", dest='config',
        required=True,
        help="release config")

    parser.add_argument("-r", "--result", dest='result',
        required=True,
        help="result file")

    parser.add_argument("-d", "--debug", dest='debug',
        action="store_true",
        help="mode")

    args = parser.parse_args()
    config = args.config
    result = args.result
    debug = args.debug

    if os.path.isdir(result):
        candidates = sum([glob.glob(os.path.join(result, e)) for e in ['*.csv', '*.json']], [])
    else:
        candidates = (result,)

    for candidate in candidates:
        print("Submit %s." % (candidate))
        worker = Worker(config=config, result=candidate, debug=debug)
        worker.run()


if __name__ == "__main__":
    main()
