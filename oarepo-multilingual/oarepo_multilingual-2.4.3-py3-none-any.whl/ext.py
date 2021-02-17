"""Multilingual extension initialization."""
from oarepo_multilingual import config


class OARepoMultilingualExt:
    """Multilingual app."""

    def __init__(self, app, db=None):
        """
        Create an instance of the extension.

        :param app      the application
        :param db       database, not used
        """
        self.init_app(app, db=None)

    def init_app(self, app, db=None):
        """
        Initialize the extension.

        :param app      the application
        :param db       database, not used
        """
        self.init_config(app)

    def init_config(self, app):
        """
        Propagate default values to the configuration.

        :param app      the application
        """
        app.config.setdefault(
            'ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE',
            config.ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE
        )
        if 'MULTILINGUAL_SUPPORTED_LANGUAGES' not in app.config and 'SUPPORTED_LANGUAGES' not in app.config:
            app.config.setdefault("MULTILINGUAL_SUPPORTED_LANGUAGES", ["_"])
        elif 'MULTILINGUAL_SUPPORTED_LANGUAGES' not in app.config:
            app.config.setdefault("MULTILINGUAL_SUPPORTED_LANGUAGES", app.config.get("SUPPORTED_LANGUAGES") + ["_"])
        elif "_" not in app.config.get('MULTILINGUAL_SUPPORTED_LANGUAGES'):
            app.config.update(MULTILINGUAL_SUPPORTED_LANGUAGES = app.config.get('MULTILINGUAL_SUPPORTED_LANGUAGES') + ["_"])


