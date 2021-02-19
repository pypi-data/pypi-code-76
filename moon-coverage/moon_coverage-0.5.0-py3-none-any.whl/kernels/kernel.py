"""Kernel module."""

from pathlib import Path
import os


class Kernel:
    """Kernel object.

    Parameters
    ----------
    name: str or pathlib.Path
        Kernel name. Symbols are accepted.

    """

    def __init__(self, name):
        self.name = name
        self.symbols = [
            part.upper() for part in Path(self.name).parts
            if part.startswith('$')
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __call__(self, **kwargs) -> str:
        """File path or URL with replaced symbols.

        Parameters
        ----------
        **kwargs: dict
            Collection of symbols to replace.

        Returns
        -------
        str
            Kernel name with replaced symbols.

        Raises
        ------
        KeyError
            If the key provided is not present in the symbols.

        Examples
        --------
        >>> kernel = Kernel('$KERNELS/fk/juice_v20.tf')

        >>> kernel(kernels='/data/juice/kernels')
        '/data/juice/kernels/fk/juice_v20.tf'

        >>> kernel(kernels='ftp://spiftp.esac.esa.int/data/SPICE/JUICE/kernels')
        'ftp://spiftp.esac.esa.int/data/SPICE/JUICE/kernels/fk/juice_v20.tf'

        """
        name = str(self.name)

        for key, value in kwargs.items():
            symbol = '$' + str(key).upper()
            if symbol in self.symbols:
                name = name.replace(symbol, str(value))
            else:
                raise KeyError(f'Symbol `{symbol}` not found in {self}')

        return name

    def __eq__(self, other):
        return str(self) == other

    def exists(self, **kwargs) -> bool:
        """Check if the file exists.

        Parameters
        ----------
        **kwargs: dict
            Collection of symbols to replace.

        Returns
        -------
        bool
            ``TRUE`` if the file exists.

        Raises
        ------
        ValueError
            If the file name is invalid (still contains symbols).

        """
        name = self(**kwargs)

        if '://' in name or '$' in name:
            raise ValueError(f'Filename invalid: `{name}`')

        return Path(name).exists()

    def encode(self, encoding='utf-8'):
        """Encode kernel name string."""
        name = str(self)

        if '$' in name:
            raise ValueError(f'Filename still contains `$` symbol: `{name}`')

        if '://' in name:
            raise ValueError(f'Filename contains `://` symbol: `{name}`')

        return name.encode(encoding=encoding)


class Kernels:
    """Available kernels.

    Parameters
    ----------
    env: str, optional
        Global environment key for kernels root folder.
        The key (`XXXX`) must be set as ``KERNELS_XXXX``
        on the system to be used as a shortcut.

        A relative/absolute path can also be provided.

        If none of them is provided, the current working
        directory will be used.

    """
    EXTENSIONS = (
        '.bc',
        '.bds',
        '.bpc',
        '.bsp',
        '.tf',
        '.ti',
        '.tls',
        '.tm',
        '.tpc',
        '.tsc',
    )

    def __init__(self, env=''):
        self.env = env
        self.path = Path(os.environ.get(f'KERNELS_{env}', env))

        if not self.path.is_dir():
            raise FolderNotFoundError(self.path)

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        nb = len(self)
        kernels = ('No kernel' if nb == 0 else f'{nb} kernel') + ('s' if nb > 1 else '')
        return f'<{self.__class__.__name__}> {kernels} found in {self}'

    def __len__(self) -> int:
        """Number of kernels available."""
        return len(self.kernels)

    def __iter__(self):
        """Iter over the all kernels available."""
        return iter(self.kernels)

    @property
    def kernels(self):
        """List all the kernels availables."""
        return [
            Kernel(str(k).replace(str(self), '$KERNELS'))
            for k in sorted(self.path.rglob('*'))
            if k.suffix in self.EXTENSIONS
        ]


class FolderNotFoundError(FileNotFoundError):
    """Folder not found custom error."""
