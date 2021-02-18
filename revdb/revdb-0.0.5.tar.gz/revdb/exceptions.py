class DBError(Exception):
    pass


class APIKeyError(DBError):
    pass


class ServiceError(DBError):
    pass


class SettingsError(DBError):
    pass
