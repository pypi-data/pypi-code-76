import spacy
import json
from .baseParser import BaseParser
from spacy.matcher import Matcher
import re


class SLParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.matcher = Matcher(self.nlp.vocab)
        pattern = [{"LOWER": {"IN": ["sl", "s/l"]}},
                   {"ORTH": {"IN": [":", " ", "@", "="]}, "OP": "*"}, {"LIKE_NUM": True}]
        pattern2 = [{"LOWER": "stop"}, {"LOWER": "loss"},
                    {"ORTH": {"IN": [":", " ", "@", "="]}, "OP": "*"}, {"LIKE_NUM": True}]
        self.matcher.add("SL", None, pattern)
        self.matcher.add("SL", None, pattern2)

    def parse_text(self, text):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        if self.debug:
            self.print_result()
        if len(self.matches) == 0:
            return ""
        _, start, end = self.matches[0]    
        span = self.doc[start:end]  # The matched span
        return re.sub(r'[^\d.]+', '', span[-1].text)
