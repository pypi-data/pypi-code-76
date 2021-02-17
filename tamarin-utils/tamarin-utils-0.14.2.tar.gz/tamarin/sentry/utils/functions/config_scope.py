from sentry_sdk import configure_scope


class Level:
    FATAL = 'fatal'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    debug = 'debug'


def config_scope(metadata, status, level):
    with configure_scope() as scope:
        scope.set_extra('status', status)
        scope.level = level
        if metadata:
            # set user
            scope.user = metadata.get(
                'user',
                {
                    'username': 'anonymous user',
                }
            )
            # set locale
            locale = metadata.get('locale', 'fa-Ir')
            scope.set_tag("page_locale", locale)
