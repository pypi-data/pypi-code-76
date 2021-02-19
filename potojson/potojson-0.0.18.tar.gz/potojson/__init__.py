from collections import OrderedDict
from json.encoder import JSONEncoder

import polib


__version__ = "0.0.18"
__title__ = "potojson"
__description__ = "Pofile to JSON conversion without pain."
__all__ = ("pofile_to_json",)


def pofile_to_json(
    content_or_filepath,
    fallback_to_msgid=False,
    fuzzy=False,
    pretty=False,
    indent=2,
    language=None,
    plural_forms=None,
    as_dict=False,
    sort_keys=False,
    **kwargs
):
    """Converts pofile by content or filepath into JSON format. Output can be
    customized using some parameters.

    :param content_or_filepath: Pofile content or filepath to be converted into
        JSON format.
    :type content_or_filepath: str

    :param fallback_to_msgid: Use msgid if translation is missing.
    :type fallback_to_msgid: bool

    :param fuzzy: Include fuzzy messages.
    :type fuzzy: bool

    :param pretty: Pretty-print JSON output.
    :type pretty: bool

    :param indent: Number of spaces for indentation used pretty-printing JSON
        output. Only takes effect if ``pretty is True``.
    :type indent: int

    :param language: Language for the translations. Will be inserted in the
        empty key of the JSON output. If not provided and the passed pofile
        includes the "Language" header, will be extracted from it.
    :type language: str

    :param plural_forms: Plural forms for the language of the translations.
        Will be insertedin the empty key of the JSON output. If not provided
        and the passed pofile includes the "Plural-Forms" header, will be
        extracted from it.
    :type language: str

    :param as_dict: Returns the output as a Python dictionary.
    :type as_dict: bool

    :param sort_keys: Sort dictionary by key. Combined with `as_dict`
        parameter, returns an instance of :py:class:`collections.OrderedDict`.
    :type sort_keys: bool

    :return: Pofile as string in JSON format.
    :rtype: str
    """
    response = {}
    po = polib.pofile(content_or_filepath)
    for entry in po:
        if entry.obsolete or (not fuzzy and entry.fuzzy):
            continue
        if entry.msgctxt:
            if entry.msgctxt not in response:
                response[entry.msgctxt] = {}
            if entry.msgid_plural:
                response[entry.msgctxt][entry.msgid] = list(
                    value
                    if value
                    else (
                        (entry.msgid_plural if i != 0 else entry.msgid)
                        if fallback_to_msgid
                        else value
                    )
                    for i, value in enumerate(entry.msgstr_plural.values())
                )
            else:
                response[entry.msgctxt][entry.msgid] = (
                    entry.msgstr
                    if entry.msgstr
                    else (entry.msgid if fallback_to_msgid else entry.msgstr)
                )
        else:
            if entry.msgid_plural:
                # ``fallback_to_msgid`` based on enumeration it's only valid
                # for most common languages the most correct way would be to
                # parse plural_forms, if provided and redirect the fallback
                # msgids accordingly, but  it's too of little benefit to add
                # such complexity
                response[entry.msgid] = list(
                    value
                    if value
                    else (
                        (entry.msgid_plural if i != 0 else entry.msgid)
                        if fallback_to_msgid
                        else value
                    )
                    for i, value in enumerate(entry.msgstr_plural.values())
                )
            else:
                response[entry.msgid] = (
                    entry.msgstr
                    if entry.msgstr
                    else (entry.msgid if fallback_to_msgid else entry.msgstr)
                )
    if not language and "Language" in po.metadata:
        language = po.metadata["Language"]
    if not plural_forms and "Plural-Forms" in po.metadata:
        plural_forms = po.metadata["Plural-Forms"]
    if language or plural_forms:
        response[""] = {}
        if language:
            response[""]["language"] = language
        if plural_forms:
            response[""]["plural-forms"] = plural_forms
    if as_dict:
        if sort_keys:
            return OrderedDict(sorted(response.items(), key=lambda item: item[0]))
        return response
    if pretty and indent is None:
        indent = 2
    return JSONEncoder(
        indent=indent if pretty else None,
        ensure_ascii=False,
        sort_keys=sort_keys,
        **kwargs
    ).encode(response)
