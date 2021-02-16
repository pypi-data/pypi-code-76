# coding: utf-8
from __future__ import unicode_literals

import spacy
import pandas as pd
from pandas.testing import assert_frame_equal
from dframcy.matcher import (
    DframCyMatcher,
    DframCyPhraseMatcher,
    DframCyDependencyMatcher,
)


dframcy_matcher = DframCyMatcher(spacy.load("en_core_web_sm"))
dframcy_phrase_matcher = DframCyPhraseMatcher(
    spacy.load("en_core_web_sm"), attr="LOWER"
)
dframcy_dependency_matcher = DframCyDependencyMatcher(spacy.load("en_core_web_sm"))


def test_matcher():
    dframcy_matcher.reset()
    pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
    dframcy_matcher.add("HelloWorld", [pattern])
    doc = dframcy_matcher.nlp("Hello, world! Hello world!")
    spacy_matcher = dframcy_matcher.matcher
    matches = spacy_matcher(doc)
    assert matches[0][0] == 15578876784678163569
    assert matches[0][1] == 0
    assert matches[0][2] == 3
    assert dframcy_matcher.nlp.vocab.strings[matches[0][0]] == "HelloWorld"
    assert doc[matches[0][1] : matches[0][2]].text == "Hello, world"

    dframcy_matcher.remove("HelloWorld")
    assert "HelloWorld" not in dframcy_matcher.matcher


def test_matcher_dataframe():
    dframcy_matcher.reset()
    pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
    dframcy_matcher.add("HelloWorld", [pattern])
    doc = dframcy_matcher.nlp("Hello, world! Hello world!")
    matches_dataframe = dframcy_matcher(doc)
    results = pd.DataFrame(
        {
            "start": [0],
            "end": [3],
            "string_id": ["HelloWorld"],
            "span_text": ["Hello, world"],
        }
    )
    assert_frame_equal(matches_dataframe, results)


def test_matcher_dataframe_multiple_patterns():
    dframcy_matcher.reset()
    dframcy_matcher.add(
        "Hello_World",
        [
            [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}],
            [{"LOWER": "hello"}, {"LOWER": "world"}],
        ],
        None,
    )
    doc = dframcy_matcher.nlp("Hello, world! Hello world!")
    matches_dataframe = dframcy_matcher(doc)
    results = pd.DataFrame(
        {
            "start": [0, 4],
            "end": [3, 6],
            "string_id": ["Hello_World", "Hello_World"],
            "span_text": ["Hello, world", "Hello world"],
        }
    )
    assert_frame_equal(matches_dataframe, results)


def test_phrase_matcher():
    patterns = [
        dframcy_phrase_matcher.nlp.make_doc(name)
        for name in ["Angela Merkel", "Barack Obama"]
    ]
    dframcy_phrase_matcher.add("Names", patterns)
    doc = dframcy_phrase_matcher.nlp("angela merkel and us president barack Obama")
    spacy_phrase_matcher = dframcy_phrase_matcher.phrase_matcher
    matches = spacy_phrase_matcher(doc)
    assert matches[0][0] == 10631222085860127603
    assert matches[0][1] == 0
    assert matches[0][2] == 2
    assert doc[matches[0][1] : matches[0][2]].text == "angela merkel"
    assert doc[matches[1][1] : matches[1][2]].text == "barack Obama"

    dframcy_phrase_matcher.remove("Names")
    assert "Names" not in dframcy_phrase_matcher.phrase_matcher


def test_phrase_matcher_dataframe():
    dframcy_phrase_matcher.reset()
    terms = ["Barack Obama", "Angela Merkel", "Washington, D.C."]
    patterns = [dframcy_phrase_matcher.nlp.make_doc(text) for text in terms]
    dframcy_phrase_matcher.add("TerminologyList", patterns)
    doc = dframcy_phrase_matcher.nlp(
        "German Chancellor Angela Merkel and US President Barack Obama "
        "converse in the Oval Office inside the White House in Washington, D.C."
    )
    phrase_matches_dataframe = dframcy_phrase_matcher(doc)
    results = pd.DataFrame(
        {
            "start": [2, 7, 19],
            "end": [4, 9, 22],
            "span_text": ["Angela Merkel", "Barack Obama", "Washington, D.C."],
        }
    )
    assert_frame_equal(phrase_matches_dataframe, results)


def test_dependency_matcher():
    pattern = [{"RIGHT_ID": "founded_id", "RIGHT_ATTRS": {"ORTH": "founded"}}]
    dframcy_dependency_matcher.add("FOUNDED", [pattern])
    doc = dframcy_dependency_matcher.nlp("Bill Gates founded Microsoft.")
    spacy_dependency_matcher = dframcy_dependency_matcher.dependency_matcher
    matches = spacy_dependency_matcher(doc)
    assert matches[0][0] == 4851363122962674176
    assert len(matches[0][1]) == 1
    assert matches[0][1][0] == 2
    assert "FOUNDED" in dframcy_dependency_matcher.dependency_matcher
    dframcy_dependency_matcher.remove("FOUNDED")
    assert "FOUNDED" not in dframcy_dependency_matcher.dependency_matcher


def test_dependency_matcher_dataframe():
    dframcy_dependency_matcher.reset()
    pattern = [{"RIGHT_ID": "founded_id", "RIGHT_ATTRS": {"ORTH": "founded"}}]
    dframcy_dependency_matcher.add("FOUNDED", [pattern])
    doc = dframcy_dependency_matcher.nlp(
        "Bill Gates founded Microsoft. And Elon Musk founded SpaceX"
    )
    dependency_matches_dataframe = dframcy_dependency_matcher(doc)
    results = pd.DataFrame(
        {"token_index": ["2", "8"], "token_text": ["founded", "founded"]}
    )
    assert_frame_equal(dependency_matches_dataframe, results)
