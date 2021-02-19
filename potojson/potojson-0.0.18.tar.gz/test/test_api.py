from collections import OrderedDict
from test import POFILE_START

import pytest

from potojson import pofile_to_json


@pytest.mark.parametrize(
    (
        "content",
        "output",
        "fallback_to_msgid",
        "fuzzy",
        "pretty",
        "indent",
        "language",
        "plural_forms",
        "as_dict",
        "sort_keys",
    ),
    (
        (
            POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n',
            '{"Hello": "Hola"}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # msgctxt
        (
            POFILE_START + 'msgctxt "Month"\nmsgid "May"\nmsgstr "Mayo"',
            '{"Month": {"May": "Mayo"}}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # obsolete
        (
            POFILE_START + '#~ msgid "May"\n#~ msgstr "Mayo"',
            "{}",
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # fallback_to_msgid
        #   True
        (
            POFILE_START + 'msgid "Hello"\nmsgstr ""\n',
            '{"Hello": "Hello"}',
            True,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        #   False
        (
            POFILE_START + 'msgid "Hello"\nmsgstr ""\n',
            '{"Hello": ""}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # msgid_plural
        (
            (
                POFILE_START + 'msgid "$n word"\nmsgid_plural "$n words"\n'
                'msgstr[0] "$n palabra"\nmsgstr[1] "$n palabras"\n'
            ),
            '{"$n word": ["$n palabra", "$n palabras"]}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # msgid_plural + msgctxt
        (
            (
                POFILE_START + 'msgctxt "a context"\nmsgid "$n word"\n'
                'msgid_plural "$n words"\nmsgstr[0] "$n palabra"\n'
                'msgstr[1] "$n palabras"\n'
            ),
            ('{"a context": {"$n word": ["$n palabra", "$n palabras"]}}'),
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # fallback_to_msgid + msgid_plural
        #   True
        (
            (
                POFILE_START + 'msgid "$n word"\nmsgid_plural "$n words"\n'
                'msgstr[0] ""\nmsgstr[1] ""\n'
            ),
            '{"$n word": ["$n word", "$n words"]}',
            True,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        #   False
        (
            (
                POFILE_START + 'msgid "$n word"\nmsgid_plural "$n words"\n'
                'msgstr[0] ""\nmsgstr[1] ""\n'
            ),
            '{"$n word": ["", ""]}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # fallback_to_msgid + msgid_plural + msgctxt
        #   True
        (
            (
                POFILE_START + 'msgctxt "a context"\nmsgid "$n word"\n'
                'msgid_plural "$n words"\nmsgstr[0] ""\nmsgstr[1] ""\n'
            ),
            ('{"a context": {"$n word": ["$n word", "$n words"]}}'),
            True,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        #   False
        (
            (
                POFILE_START + 'msgctxt "a context"\nmsgid "$n word"\n'
                'msgid_plural "$n words"\nmsgstr[0] ""\nmsgstr[1] ""\n'
            ),
            ('{"a context": {"$n word": ["", ""]}}'),
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # fuzzy
        #   True
        (
            POFILE_START + '#, fuzzy\nmsgid "Hello"\nmsgstr "Hola"\n',
            '{"Hello": "Hola"}',
            False,
            True,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        #   False
        (
            POFILE_START + '#, fuzzy\nmsgid "Hello"\nmsgstr "Hola"\n',
            "{}",
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        # pretty
        (
            POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n',
            '{\n  "Hello": "Hola"\n}',
            False,
            False,
            True,
            None,
            None,
            None,
            False,
            False,
        ),
        # pretty with custom indent
        (
            POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n',
            '{\n   "Hello": "Hola"\n}',
            False,
            False,
            True,
            3,
            None,
            None,
            False,
            False,
        ),
        # language
        #   discover from pofile
        (
            POFILE_START + '"Language: es\\n"\n\n',
            '{"": {"language": "es"}}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        #   specified in keyword argument
        (
            POFILE_START,
            '{"": {"language": "es"}}',
            False,
            False,
            False,
            None,
            "es",
            None,
            False,
            False,
        ),
        # plural_forms
        #   discover from pofile
        (
            POFILE_START + '"Plural-Forms: nplurals=2; plural=n != 1;\\n"\n\n',
            '{"": {"plural-forms": "nplurals=2; plural=n != 1;"}}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
        #   specified in keyword argument
        (
            POFILE_START,
            '{"": {"plural-forms": "nplurals=2; plural=n != 1;"}}',
            False,
            False,
            False,
            None,
            None,
            "nplurals=2; plural=n != 1;",
            False,
            False,
        ),
        # as dict
        (
            POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n',
            {"Hello": "Hola"},
            False,
            False,
            False,
            None,
            None,
            None,
            True,
            False,
        ),
        # sort_keys
        #   as JSON
        (
            (POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\nmsgid "A"\nmsgstr "B"\n'),
            '{"A": "B", "Hello": "Hola"}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            True,
        ),
        #   as_dict
        (
            (POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\nmsgid "A"\nmsgstr "B"\n'),
            OrderedDict({"A": "B", "Hello": "Hola"}),
            False,
            False,
            False,
            None,
            None,
            None,
            True,
            True,
        ),
        # Non ASCII characters
        (
            (POFILE_START + 'msgid "Coal"\nmsgstr "Carbón"\n'),
            '{"Coal": "Carbón"}',
            False,
            False,
            False,
            None,
            None,
            None,
            False,
            False,
        ),
    ),
)
def test_pofile_content_to_json(
    content,
    output,
    fallback_to_msgid,
    fuzzy,
    pretty,
    indent,
    language,
    plural_forms,
    as_dict,
    sort_keys,
):
    assert (
        pofile_to_json(
            content,
            fallback_to_msgid=fallback_to_msgid,
            fuzzy=fuzzy,
            pretty=pretty,
            indent=indent,
            language=language,
            plural_forms=plural_forms,
            as_dict=as_dict,
            sort_keys=sort_keys,
        )
        == output
    )
