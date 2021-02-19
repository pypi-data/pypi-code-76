import pytest
from slackertpy import blocks


def test_add_section_text_too_long():
    s = blocks.Section()
    with pytest.raises(ValueError):
        s.add_field_text('s' * 3001)


def test_add_field_text_too_long():
    s = blocks.Section()
    with pytest.raises(ValueError):
        s.add_field_text('s' * 2001)
