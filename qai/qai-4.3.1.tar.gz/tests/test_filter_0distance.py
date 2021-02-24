import pytest

from qai.qconnect.qallback import _filter_0distance


# for when we expect a test to fail
xfail = pytest.mark.xfail

segment_good = "He visits the store."
segment_needs_uc = "he visits the store."
start, end = 0, 9

issues = [{"from": start, "until": end, "suggestions": ["He visits"]}]
issues_with_one_0distance_and_one_good_suggestion = [
    {"from": start, "until": end, "suggestions": ["He visits", "They visit"]}
]


@xfail(raises=KeyError)
def test_issue_without_suggestions():
    """
    This is a known bug that we should fix
    If an issue doesn't have a suggestions key, we get an unhandled exception
    """
    bad_issue = [{"from": start, "until": end}]
    assert _filter_0distance(segment_good, bad_issue)


def test_it_filters_0_distance():
    assert (
        _filter_0distance(segment_good, issues) == []
    ), "it should filter a no-op suggestion"


def test_it_only_filters_0_distance_when_there_are_multiple_suggestions():
    assert _filter_0distance(
        segment_good, issues_with_one_0distance_and_one_good_suggestion
    ) == [{"from": 0, "until": 9, "suggestions": ["They visit"]}]


def test_it_doesnt_filter_capitalization_correction():
    assert (
        _filter_0distance(segment_needs_uc, issues) == issues
    ), "It shouldn't filter capitalization correction"

