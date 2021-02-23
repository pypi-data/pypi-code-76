__all__ = [
    'Section'
]


class Section:
    def __init__(self, mapping: dict):
        self._dict = mapping

    def __getitem__(self, key: str):
        try:
            if '.' in key:
                pathSegments = key.split(".")
                value = self._dict[pathSegments[0]]
                for pathSegment in pathSegments[1:]:
                    value = value[pathSegment]
            else:
                value = self._dict[key]

            if isinstance(value, dict):
                return Section(value)
            else:
                return value
        except KeyError:
            raise AttributeError(key)

    def __getattr__(self, key: str):
        try:
            value = self._dict[key]
            if isinstance(value, dict):
                return Section(value)
            else:
                return value
        except KeyError:
            raise AttributeError(key)
