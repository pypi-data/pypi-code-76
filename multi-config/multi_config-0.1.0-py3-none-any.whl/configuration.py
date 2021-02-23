from .section import Section

__all__ = [
    'Configuration'
]


class Configuration(Section):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
