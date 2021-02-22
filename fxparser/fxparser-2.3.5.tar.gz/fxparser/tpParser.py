import spacy
import json
from .baseParser import BaseParser
from spacy.matcher import Matcher
import re


class TPParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.matcher = Matcher(self.nlp.vocab)
        pattern = [{"LOWER": {"IN": ["tp", "t/p", "tp1", "tp2", "tp3", "tp4", "tp5"]}}, {"IS_DIGIT": True, "OP": "*"},
                   {"ORTH": {"IN": [":", " ", "@", "="]}, "OP": "*"}, {"LIKE_NUM": True}]
        pattern2 = [{"LOWER": "take"}, {"LOWER": "profit"},
                    {"ORTH": {"IN": [":", " ", "@"]}, "OP": "*"}, {"LIKE_NUM": True}]
        self.matcher.add("TP", None, pattern)
        self.matcher.add("TP", None, pattern2)

    def parse_text(self, text):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        # self.explain(text)
        if self.debug:
            self.print_result()
        tps = []
        maxLength = max(b-a for _, a, b in self.matches) if len(self.matches) > 0 else 0
        for _, start, end in self.matches:
            length = end - start
            if length < maxLength:
                continue
            span = self.doc[start:end]  # The matched span
            tmpPrice = span[-1].text
            tps.append(re.sub(r'[^\d.]+', '', tmpPrice))

        return tps
