"""
``djangorestframework`` (DRF) related configuration values. DRF uses a single dict to describe all of its options and configurations, so be careful not to overwrite this in your settings file.
"""

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}
"""
A DRF configuration dict. By default, it changes ``camelCase`` to ``snake_case`` in request data, and does the opposite for response data. This is to let you keep language-consistent styling in Python and JavaScript code.
"""
