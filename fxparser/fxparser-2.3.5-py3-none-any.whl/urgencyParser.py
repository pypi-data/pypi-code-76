import spacy
import json
from .baseParser import BaseParser
from spacy.matcher import PhraseMatcher

class UrgencyParser(BaseParser):
    def __init__(self):
        super().__init__()
        keywords = ["now", "instant"]
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(name) for name in keywords]

        self.matcher.add("Urgency", None, *patterns)

    def parse_text(self,text):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        if self.debug:
            self.print_result()
        return len(self.matches) > 0
    