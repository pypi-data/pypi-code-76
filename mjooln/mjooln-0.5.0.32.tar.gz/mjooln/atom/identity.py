import uuid

from mjooln.core.seed import Seed
from mjooln.core.glass import Glass


class IdentityError(Exception):
    pass


class Identity(str, Seed, Glass):
    """ UUID string generator with convenience functions

    Inherits str, and is therefore an immutable string, with a fixed format
    as illustrated below.

    Examples::

        Identity()
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

        Identity.is_in('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            True

        Identity.find_one('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

    """

    REGEX = r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}' \
            r'\_[0-9A-F]{12}'
    LENGTH = 36

    @classmethod
    def from_seed(cls, str_: str):
        return cls(str_)

    def __new__(cls,
                identity: str = None):
        if not identity:
            identity = str(uuid.uuid4()).replace('-', '_').upper()
        elif not cls.is_seed(identity):
            raise IdentityError(f'String is not valid identity: {identity}')
        instance = super().__new__(cls, identity)
        return instance

    def __repr__(self):
        return f'Identity(\'{self}\')'

    @classmethod
    def elf(cls, identity):
        if isinstance(identity, Identity):
            return identity
        elif isinstance(identity, str):
            return cls.find_seed(identity)
        else:
            return cls()