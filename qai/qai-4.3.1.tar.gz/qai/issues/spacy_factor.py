import traceback
from typing import List, Optional, Tuple

from qai.issues.issues import make_issue

try:
    from spacy.tokens.span import Span
except ModuleNotFoundError as e:
    print(
        "\n\nQAI v2.0.0 and above assume spaCy is installed, but do not list it as a requirement"
        "If you want to use SpacyFactor, please install spaCy >=2.1.0\n\n"
    )
    raise e


class SpacyFactor(object):
    def __init__(
            self,
            issue_type: str,
            simple_description: str,
            description: Optional[str] = None,
            debug=False,
    ):
        self.issue_type = issue_type
        self.simple_description = simple_description
        if description:
            self.description = description
        self.debug = debug

    @staticmethod
    def match_case(span: Span, suggestions):
        """
        suggestions respect original casing
        ex. purchase -> buy (lower)
        ex. PURCHASE -> BUY (upper)
        ex. Purchase -> Buy (title)
        """
        span_text = span.text
        try:
            if len(span_text.strip()):
                words = span_text.split(" ")
                is_sent_start = len(span) and span[0].is_sent_start
                if words[0].islower():
                    # this should exclude I
                    # todo - capitalized proper nouns
                    suggestions = [
                        " ".join(
                            [
                                word.lower() if word != "I" else word
                                for word in sug.split()
                            ]
                        )
                        for sug in suggestions
                    ]
                elif len(words[0]) > 1 and words[0].isupper():
                    # len condition is to exclude capitalization caused by "I"
                    suggestions = [s.upper() for s in suggestions]
                elif (len(words[0]) > 1 and words[0][0].isupper()) or (
                        is_sent_start and len(span[0]) == 1
                ):
                    # title case - first letter check & conversion due to contractions
                    for i, s in enumerate(suggestions):
                        if len(s.strip()):
                            s_words = s.split(" ")
                            suggestions[i] = " ".join(
                                [s_words[0][0].upper() + s_words[0][1:]] + s_words[1:]
                            ).strip()
        except:
            suggestions_log = ",".join(suggestions)
            print(traceback.format_exc())
            print(f"Case matching failed for span: {span_text} and {suggestions_log}")

        return suggestions

    def __call__(
            self, spacy_span: Span, meta_subcategory=None, describer=None, cased=True
    ):
        """
        convenient wrapper around make_issue if you are using spaCy

        usage example:

        ```python
        from spacy.tokens import Span
        from app.factor import SpacyFactor


        SOV = SpacyFactor(
            "subject_object_verb_spacing",
            "Keep the subject, verb, and object of a sentence close together to help the reader understand the sentence."
        )

        Span.set_extension("score", default=0)
        Span.set_extension("suggestions", default=[])

        doc = nlp("Holders of the Class A and Class B-1 certificates will be entitled to receive on each Payment Date, to the extent monies are available therefor (but not more than the Class A Certificate Balance or Class B-1 Certificate Balance then outstanding), a distribution.")
        score = analyze(doc)
        if score is not None:
            span = Span(doc, 0, len(doc))  # or whichever TOKENS are the issue (don't have to worry about character indexes)
            span._.score = score
            span._.suggestions = get_suggestions(doc)
            issues = SOV(span)
        ```
        """
        text, start, end = spacy_span.text, spacy_span.start_char, spacy_span.end_char
        score = spacy_span._.score if spacy_span.has_extension("score") else 0
        suggestions = (
            spacy_span._.suggestions if spacy_span.has_extension("suggestions") else []
        )

        learn_more = (
            spacy_span._.learn_more if spacy_span.has_extension("learn_more") else ""
        )
        paragraph = (
            spacy_span._.paragraph if spacy_span.has_extension("paragraph") else False
        )
        header = spacy_span._.header if spacy_span.has_extension("header") else ""
        meta_dict = (
            spacy_span._.meta_dict if spacy_span.has_extension("meta_dict") else {}
        )
        visible = (spacy_span._.visible if spacy_span.has_extension("visible") else True)
        # SIMPLE DESCRIPTION IS DIFFERENT, since it is set when initialized
        # so we need to check that the span doesn't just have an empty value
        simple_description = (
            spacy_span._.simple_description
            if (
                    spacy_span.has_extension("simple_description")
                    and spacy_span._.simple_description != ""
            )
            else self.simple_description
        )
        accept_all_changes = (
            spacy_span._.accept_all_changes
            if spacy_span.has_extension("accept_all_changes")
            else False
        )

        if cased:
            suggestions = self.match_case(spacy_span, suggestions)

        if describer:
            description = describer(spacy_span)
        else:
            description = self.description

        if meta_subcategory:
            subcategory = meta_subcategory
        else:
            subcategory = ""

        return make_issue(
            text,
            start,
            end,
            issue_type=self.issue_type,
            score=score,
            description=description,
            simpleDescription=simple_description,
            suggestions=suggestions,
            subCategory=subcategory,
            learnMore=learn_more,
            paragraph=paragraph,
            header=header,
            metaDict=meta_dict,
            accept_all_changes=accept_all_changes,
            debug=self.debug,
            segment=spacy_span.doc.text,
            visible=visible
        )
