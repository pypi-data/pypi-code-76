# -*- coding: utf-8 -*- #
"""Simple test of version import."""
def handler(type=None, resource=None, id=None, json_pointer=None,
            app=None, content=None, root=None, content_pointer=None):
    """Use this function as handler."""
    languages = list(app.config.get("MULTILINGUAL_SUPPORTED_LANGUAGES", []))

    default_template = app.config.get("ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE", {})
    template = app.config.get("ELASTICSEARCH_LANGUAGE_TEMPLATES", {})

    data_dict= dict()
    for language in languages:
        if id is not None:
            language_with_context = language + '#' + id
            if language_with_context in template.keys():
                data_dict[language] = template[language_with_context]
                continue
        data_dict[language] = template.get(language, default_template)


    return {
        "type": "object",
        "properties": data_dict
    }
