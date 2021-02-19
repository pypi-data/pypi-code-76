"""SPICE kernel pool module."""

import spiceypy as sp

from ..misc import logger


log_spice_pool, debug_spice_pool = logger('SPICE Pool')


class MetaSPICEPool(type):
    """Meta SPICE kernel pool object."""
    # pylint: disable=no-value-for-parameter, unsupported-membership-test

    def __repr__(cls):
        n = int(cls)
        if n == 0:
            desc = 'EMPTY'
        else:
            desc = f'{n} kernel'
            desc += 's'
            desc += ' loaded:\n - '
            desc += '\n - '.join(cls.kernels)

        return f'<{cls.__name__}> {desc}'

    def __int__(cls):
        return cls.count()

    def __len__(cls):
        return cls.count()

    def __hash__(cls):
        return cls.get_pool_hash()

    def __eq__(cls, other):
        if isinstance(other, str):
            return cls == [other]

        if isinstance(other, list):
            return cls == tuple(other)

        return hash(cls) == hash(other)

    def __iter__(cls):
        return iter(cls.kernels)

    def __contains__(cls, el):
        return cls.contains(el)

    def __add__(cls, el):
        return cls.add(el)

    def __sub__(cls, el):
        return cls.remove(el)

    @staticmethod
    def count():
        """Count the number of kernels in the pool."""
        return sp.ktotal('ALL')

    def get_pool(cls):
        """Get SPICE kernel pool files."""
        return tuple([
            sp.kdata(i, 'ALL')[0] for i in range(cls.count())
        ])

    def get_pool_hash(cls):
        """Get SPICE pool content hash."""
        return hash(cls.get_pool())

    @property
    def kernels(cls):
        """Return the lis of kernels loaded in the pool."""
        return cls.get_pool()

    def contains(cls, kernel):
        """Check if the kernel is in the pool."""
        return kernel in cls.kernels

    def add(cls, kernel, purge=False):
        """Add a kernel to the pool."""
        if purge:
            cls.purge()

        if kernel in cls:
            raise ValueError(f'Kernel `{kernel}` is already in the pool.')

        log_spice_pool.debug('Add %s', kernel)
        sp.furnsh(kernel)

    def remove(cls, kernel):
        """Remove the kernel from the pool if present."""
        if kernel not in cls:
            raise ValueError(f'Kernel `{kernel}` is not in the pool.')

        log_spice_pool.debug('Remove %s', kernel)
        sp.unload(kernel)

    @staticmethod
    def purge():
        """Purge the pool from all its content."""
        log_spice_pool.info('Empty the pool')
        sp.kclear()


class SPICEPool(metaclass=MetaSPICEPool):
    """SPICE kernel pool object."""
