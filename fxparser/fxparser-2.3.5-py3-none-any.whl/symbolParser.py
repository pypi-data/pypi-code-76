import spacy
import json
from pathlib import Path
from .baseParser import BaseParser
from spacy.matcher import PhraseMatcher
import re


class SymbolParser(BaseParser):
    def __init__(self):
        super().__init__()
        forex_path = "assets/forexlist.json"
        forex_data = json.loads(
            Path(__file__).parent.joinpath(forex_path).read_text())

        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(name) for name in forex_data]

        self.matcher.add("Symbol", None, *patterns)

    def parse_text(self, text):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        if self.debug:
            self.print_result()
        if len(self.matches) == 0:
            return ""
        _, start, end = self.matches[0]
        span = self.doc[start:end]
        return re.sub(r'\W+', '', span.text).upper()
