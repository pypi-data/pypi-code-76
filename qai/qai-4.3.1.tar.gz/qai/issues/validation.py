import re

from typing import List

from spacy.tokenizer import Tokenizer


class Validator:
    html_pattern = re.compile("<.*?>")
    non_letter_pattern = re.compile("[^a-zA-Z'\-\s]")
    acceptable_fraction_of_ignorable_tokens = 0.5

    def __init__(
        self, nlp_obj, sentence_token_limit=1024, ignore_html=True,
    ):
        self.sentence_token_limit = sentence_token_limit
        self.ignore_html = ignore_html
        self.nlp = self.confirm_nlp(nlp_obj)
        self.tokenizer = Tokenizer(self.nlp.vocab)

    def confirm_nlp(self, nlp_obj):
        if not nlp_obj:
            # make the minimal nlp instance needed for SBD
            from spacy.lang.en import English

            nlp = English()  # just the language with no model
            sentencizer = nlp.create_pipe("sentencizer")
            nlp.add_pipe(sentencizer, first=True)
        elif "parser" in nlp_obj.pipe_names:
            # spaCy uses the parser to do SBD
            # so if parser is in the pipe, SBD will happen
            nlp = nlp_obj
        else:
            # we actually need to add SBD to the spacy instance
            # Sentencizer has to be first in the pipeline or you get the error:
            # "ValueError: [E043] Refusing to write to token.sent_start if its document is parsed,
            # because this may cause inconsistent state.""
            nlp = nlp_obj.add_pipe(nlp_obj.create_pipe("sentencizer"), first=True)
        return nlp

    def has_html(self, segment: str):
        return self.html_pattern.match(segment) != None

    def has_non_letter(self, segment: str):
        return self.non_letter_pattern.match(segment) != None

    def is_empty(self, segment: str):
        return len(segment.strip()) == 0

    def has_sentence_over_length_limit(self, segment: str):
        too_long = False
        for sent in self.nlp(segment).sents:
            if len(sent) > self.sentence_token_limit:
                too_long = True
        return too_long

    def is_unnacceptable(self, segment: str):
        is_garbage = False

        if self.ignore_html and self.has_html(segment) is True:
            is_garbage = True

        if self.is_empty(segment):
            is_garbage = True

        if self.has_sentence_over_length_limit(segment):
            is_garbage = True

        return is_garbage

    def _get_ignored_tokens(self, segment: str) -> List[str]:
        ignored_tokens = []
        for token in self.tokenizer(segment):
            if token.like_url:
                ignored_tokens.append(token.text)
            elif "=" in token.text:
                ignored_tokens.append(token.text)
            elif self.has_non_letter(token.text):
                ignored_tokens.append(token.text)
        return ignored_tokens

    def has_too_many_ignore_tokens(self, segment: str) -> bool:
        token_length = len(self.nlp(segment.strip()))
        ignored_tokens = self._get_ignored_tokens(segment)
        ignored_length = len(ignored_tokens)
        if token_length == 0:
            return False
        else:
            return (
                ignored_length / token_length
                > self.acceptable_fraction_of_ignorable_tokens
            )

    def __call__(self, segment: str):
        is_valid = True
        if self.is_unnacceptable(segment):
            is_valid = False
        if self.has_too_many_ignore_tokens(segment):
            is_valid = False
        return is_valid
