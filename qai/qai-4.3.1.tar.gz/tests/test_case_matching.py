from typing import List

import en_core_web_sm
import pytest
from spacy.tokens import Span

from qai.issues.spacy_factor import SpacyFactor


nlp = en_core_web_sm.load()


@pytest.mark.parametrize(
    "span,suggestions,corrected",
    [
        (
            nlp("A majority of apps will not require any changes")[:3],
            ["most", "most of"],
            ["Most", "Most of"],
        ),
        (nlp("A certain fraction of")[:], ["a portion"], ["A portion"],),
        (nlp("A sufficient number of elephants.")[:3], ["enough"], ["Enough"]),
        (nlp("Hey, you suck")[2:], ["I suck"], ["I suck"]),
    ],
)
def test_case_starts_with_a_or_I(
    span: Span, suggestions: List[str], corrected: List[str]
):
    fixed_suggestions = SpacyFactor.match_case(span, suggestions)
    assert (
        fixed_suggestions == corrected
    ), f"Should title case if span starts with {span[0].text}"

