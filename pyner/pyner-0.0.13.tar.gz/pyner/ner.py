#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wang, Bodhi Faqun <jyxz5@hotmail.com>
#
"""ner

This program is SDK of Ner service API.

It can handle one sentence or simple text file by self-NER or stanford NER service

For instance:
$ python ner.py --help
usage: ner.py [-h] [--nertype NERTYPE] [--classifier CLASSIFIER]
              [--endpoint ENDPOINT] [--sentence SENTENCE] [--path PATH]

Process one sentence and simple textfile by remote self-NER service or
Stanford NER one.

optional arguments:
  -h, --help            show this help message and exit
  --nertype NERTYPE     NER service type,self:self-
                        NER(defualt),stanford:tanford-NER
  --classifier CLASSIFIER
                        classifier code of Stanford NER service,including
                        7class, 4class, 3class, distsim
  --endpoint ENDPOINT   Endpoint of self-NER service,ignored when Stanford-NER
                        type
  --sentence SENTENCE   Sentence to process
  --path PATH           Path file to process

$ python ner.py --endpoint http://example.com/ner/bert/normal --path test.txt --sentence '康龙化成(03759)拟续聘安永华明为2020年度境内会计师事 务所'
{'ORG': ['康龙化成', '安永华明']}
{'LOC': ['新冠', '新疆'],
 'ORG': ['华资实业',
         '明科',
         '中葡',
         '亚星',
         '厦华',
         '中房股份',
         '中房股份',
         '西域旅游',
         '西域旅游',
         '丰华股份',
         '丰华股份',
         '壳公司']}

$ python ner.py --nertype stanford --sentence 'hello, chongqing, intel, IBM, Tecent. Bill Gates said.' --classifier 7class
{'LOC': ['chongqing'],
 'ORG': ['intel', 'IBM', 'Tecent'],
 'PER': ['Gates']}

$ python ner.py --nertype stanford --classifier 7class  --path pg14469.txt
"""
__author__ = "Wang Bodhi Faqun<jyxz5@hotmail.com>"
__copyright__ = "Copyright 2021 Wang Bodhi Faqun"
__license__ = "MIT"
__version__ = "0.0.13"

import requests
from jsonmerge import merge
from lxml import html
from bs4 import BeautifulSoup


class basener:
    schema = {
             "properties": {
                 "LOC": {
                     "mergeStrategy": "append"
                 },
                 "ORG": {
                     "mergeStrategy": "append"
                 },
                 "PER": {
                     "mergeStrategy": "append"
                 }
            }
        }

    def __init__(self):
        self.endpoint = ""
        pass

    def getEndpoint(self):
        return self.endpoint

    def ner_sentence(self, sentence:str):
        pass

    def ner_file(self, path:str, encoding="utf-8"):
        with open(path, "r", encoding=encoding) as f:
            lines = f.read()

        return self.ner_sentence(lines)


class ner(basener):
    def __init__(self, endpoint:str):
        self.endpoint = endpoint

    def ner_sentence(self, sentence:str):
        r = requests.post(self.endpoint,
                          json={'sentence':sentence})
        if not r.ok:
            raise Exception('[ner_sentence]\n{}'.format(r.text))

        return r.json()

    def ner_file(self, path:str, encoding:str="utf-8"):
        with open(path, "r", encoding=encoding) as f:
            lines = f.readlines()
        lines = [ line.strip() for line in lines if line.strip()!='']

        result = dict()
        for line in lines:
            r=self.ner_sentence(line)
            if r != dict():
                result = merge(result, r, self.schema)

        return result


class stanford_ner(basener):

    classifiers = {'7class':'english.muc.7class.distsim.crf.ser.gz',
                   '4class':'english.conll.4class.distsim.crf.ser.gz',
                   '3class':'english.all.3class.distsim.crf.ser.gz',
                   'distsim':'chinese.misc.distsim.crf.ser.gz'
                   }
    xpath = '/html/body/text()'
    tag   = 'wi'
    entities = {'LOC': {"entity":"LOCATION"},
                'PER': {"entity":"PERSON"},
                'ORG': {"entity":"ORGANIZATION"}
               }


    def __init__(self, classifier):
        self.endpoint = "http://nlp.stanford.edu:8080/ner/process"
        if classifier not in stanford_ner.classifiers.keys():
            raise ValueError('Unsported classifier {}'.format(classifier))
        self.classifier = stanford_ner.classifiers[classifier]
        self.outputFormat = "xml"
        self.preserveSpacing = "true"

    def getEndpoint(self):
        return self.endpoint

    def ner_sentence(self, sentence:str):
        self.input = sentence
        params = {'classifier':self.classifier,
                  'outputFormat': self.outputFormat,
                  'preserveSpacing':self.preserveSpacing,
                  'input':self.input
                  }
        result = dict()

        r = requests.post(self.endpoint, data=params)
        if not r.ok:
            raise Exception('[ner_sentence]\n{}'.format(r.text))

        tree = html.fromstring(r.content)
        ner_result = tree.xpath(stanford_ner.xpath)[1]
        bsObj = BeautifulSoup(ner_result.strip(),"lxml")
        for k,v in stanford_ner.entities.items():
            result[k]= [ item.get_text() for item in bsObj.findAll(stanford_ner.tag,v) ]

        return result

    def ner_file(self, path:str, encoding:str="utf-8", maxlines:int=50):
        with open(path, "r", encoding=encoding) as f:
            lines = f.readlines()

        lines = [ line.strip() for line in lines if line.strip()!='']

        result = dict()
        start = 0
        end = len(lines)
        while start < end:
            block = str(lines[start:start + maxlines])
            result0 = {'LOC': [], 'PER': [], 'ORG': []}
            r=self.ner_sentence(block)
            if r != result0:
                result = merge(result, r, self.schema)
            start = start + maxlines

        return result

def main():
    from pprint import pprint
    import pybase64, argparse, os, sys

    default_ner_endpoint= pybase64.b64decode(
        b'aHR0cDovL2RhaS5kZWxvaXR0ZS5jb206MzA1MDAvbmVyL2JlcnQvbm9ybWFs').decode("utf-8")

    nertypes = ("self","stanford")

    """Entry point of the program when called as a script.
    """
    # Parse command line options
    parser = argparse.ArgumentParser (description=
                    """Process one sentence and simple text"""
                    """file by remote self-NER service or Stanford NER one.""")
    parser.add_argument ('--nertype', dest='nertype',
                         help='NER service type,self:self-NER(defualt),stanford:tanford-NER')
    parser.add_argument ('--classifier', dest='classifier',
                         help="""classifier code of Stanford NER service,including """
                              """7class, 4class, 3class, distsim"""
                              )
    parser.add_argument ('--endpoint', dest='endpoint',
                         help='Endpoint of self-NER service,ignored when Stanford-NER type')
    parser.add_argument ('--sentence', dest='sentence',
                         help='Sentence to process')
    parser.add_argument ('--path', dest='path',
                         help='Path file to process')
    args = parser.parse_args ()
    nertype = args.nertype.lower() if args.nertype is not None else None
    if nertype is None or nertype in ['','self','default']:
        nertype = 'self'
    elif nertype not in nertypes:
        raise ValueError("Unsported NER type[{}] inputed!".format(nertype))

    if nertype == 'self':
        endpoint = args.endpoint
        if endpoint is None:
            try:
                endpoint = os.getenv ("NER_ENDPOINT", default_ner_endpoint)
            except Exception as e:
                print("[getenv]{}".format(e))
                sys.exit(1)
    elif nertype == 'stanford':
        classifier = args.classifier

    sentence = args.sentence
    path = args.path

    if sentence is None and path is None:
        print("Please input sentence or file name to process!")
        parser.print_help()
        sys.exit(1)


    obj = ner (endpoint) if nertype == 'self' else stanford_ner(classifier)

    if sentence is not None:
        try:
            result = obj.ner_sentence(sentence)
            pprint(result, width=40)
        except Exception as e:
            print("[sentence]{}".format(e))
            sys.exit(1)

    if path is not None:
        try:
            result = obj.ner_file(path)
            pprint(result)
        except Exception as e:
            print("[file]{}".format(e))
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
