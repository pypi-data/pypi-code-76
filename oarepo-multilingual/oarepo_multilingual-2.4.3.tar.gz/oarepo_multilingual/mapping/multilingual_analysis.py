# -*- coding: utf-8 -*- #
"""Handler for multilingual analyzer."""
import json

from deepmerge import always_merger


def multilingual_analysis(type=None, resource=None, id=None, json_pointer=None,
                          app=None, content=None, root=None, content_pointer=None):
    """Use this function as handler."""
    languages = list(app.config.get("MULTILINGUAL_SUPPORTED_LANGUAGES", []))

    analyzer = app.config.get("ELASTICSEARCH_LANGUAGE_ANALYSIS", {})

    analysis_list = list()

    for language in languages:
        if id is not None:
            language_with_context = language + '#' + id
            if language_with_context in analyzer.keys():
                analysis_list.append(analyzer[language_with_context])
        elif language in analyzer.keys():
            analysis_list.append(analyzer[language])

    if not analysis_list:
        return {}

    result = {}
    for i in analysis_list:
        always_merger.merge(result, i)


    return result
