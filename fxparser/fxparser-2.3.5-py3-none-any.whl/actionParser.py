import spacy
import json
from pathlib import Path
from .baseParser import BaseParser
from spacy.matcher import PhraseMatcher


class ActionParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.actions = ["buy", "sell"]
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(name) for name in self.actions]
        self.matcher.add("Action", None, *patterns)

    def parse_text(self, text):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        debug = self.debug
        if debug:
            self.print_result()
        if len(self.matches) == 0:
            return ""
        _, start, end = self.matches[0]
        span = self.doc[start:end]
        return span.text.upper()
