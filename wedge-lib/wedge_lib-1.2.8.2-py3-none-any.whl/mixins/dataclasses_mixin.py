from dataclasses import asdict


class DataclassMixin:
    def to_dict(self):
        return asdict(self)  # noqa

    def __str__(self):
        return str(self.to_dict())
