"""Metakernel module."""

from pathlib import Path

from .kernel import Kernel
from .parser import read_kernel
from ..misc import wget


class MetaKernel:
    """Metakernel object.

    Parameters
    ----------
    name: str or pathlib.Path
        Metakernel file name.
    **kwargs: dict
        Kernels variables to override.

    """

    def __init__(self, name, **kwargs):
        self.fname = name
        self.__kwargs = {k.upper(): v for k, v in kwargs.items()}

    def __str__(self):
        return self.fname.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __iter__(self):
        for kernel in self.kernels:
            yield kernel(**self._kwargs())

    def __call__(self, **kwargs):
        """Iterator with custom keywords."""
        for kernel in self.kernels:
            yield kernel(**self._kwargs(kwargs))

    @property
    def fname(self) -> str:
        """Metakernel file name."""
        return self.__fname

    @fname.setter
    def fname(self, name):
        """Metakernel file name setter."""
        self.name = name
        self.__fname = Path(name)
        self.__content, self.__data, self.__kwargs = None, None, None
        self.__kernels = None

        if not self.exists():
            raise FileNotFoundError(self.fname)

    def _load(self):
        """Load content and parse data."""
        self.__content, self.__data = read_kernel(self.fname)

        # Save symbols and values as default kwargs if pressent
        if 'PATH_SYMBOLS' in self.data and 'PATH_VALUES' in self.data:
            self.__kwargs = {
                **dict(zip(self.data['PATH_SYMBOLS'], self.data['PATH_VALUES'])),
                **self.__kwargs,
            }

        # Override original values
        self.data['PATH_SYMBOLS'] = list(self.__kwargs.keys())
        self.data['PATH_VALUES'] = list(self.__kwargs.values())

    def exists(self):
        """Check if the file exists locally."""
        return self.fname.exists()

    @property
    def content(self) -> str:
        """File full content."""
        if self.__content is None:
            self._load()
        return self.__content

    @property
    def data(self) -> dict:
        """File parsed data."""
        if self.__data is None:
            self._load()
        return self.__data

    @property
    def kernels(self) -> list:
        """Kernels to load."""
        if self.__kernels is None:
            self.__kernels = [Kernel(k) for k in self.data.get('KERNELS_TO_LOAD', [])]
        return self.__kernels

    @property
    def ftp(self) -> str:
        """Main FTP URL source."""
        ftp = [line.strip() for line in self.content.splitlines() if 'ftp://' in line]

        if not ftp:
            raise KeyError('FTP URL not found.')

        if len(ftp) > 1:
            raise ValueError(f'Multiple FTP URL found: `{ftp}`')

        return ftp[0]

    def _kwargs(self, kwargs=None) -> dict:
        """Merge keyword arguments.

        Priority order (lower to higher):
            - Metakernel symbols (``PATH_SYMBOLS`` and ``PATH_VALUES``)
            - Class kwargs
            - Method kwargs

        """
        if self.__data is None:
            self._load()

        return {
            **self.__kwargs,
            **{k.upper(): v for k, v in kwargs.items()}
        } if kwargs is not None else self.__kwargs

    def check(self, download=False, **kwargs) -> dict:
        """Check if all the kernels are locally availables.

        Parameters
        ----------
        download: bool, str
            Download all the missing kernels.
        **kwargs: dict, optional
            Symbolic variable(s) to override.

        Returns
        -------
        List of `found` and `missing` kernels.

        Raises
        ------
        FileNotFoundError
            If the kernel is missing locally.

        """
        kwargs = self._kwargs(kwargs)

        kernels = {'missing': [], 'found': []}
        for kernel in self.kernels:
            if kernel.exists(**kwargs):
                kernels['found'].append(kernel)
            else:
                kernels['missing'].append(kernel)

        if download:
            for kernel in kernels['missing']:
                url = kernel(kernels=self.ftp)
                fout = kernel(**kwargs)
                wget(url, fout)

            kernels['found'].extend(kernels['missing'])
            kernels['missing'] = []

        return kernels
