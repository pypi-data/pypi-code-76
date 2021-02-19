"""CReMA module."""

from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen

from .vars import DATA
from ..kernels import MetaKernel
from ..misc import wget, logger


log_esa_crema, debug_esa_crema = logger('ESA CReMA', info_stdout=True)


class CReMACollection(type):
    """Collection of Consolidated Report on Mission Analysis (CReMA).

    See Also
    --------
    JUICE_CReMA

    """
    # pylint: disable=no-value-for-parameter, not-an-iterable, unsubscriptable-object
    # pylint: disable=no-member, unsupported-membership-test

    URL = None      # Main kernels listing
    CSV = None      # Cached CReMAs csv list

    __mk = {}

    def __str__(cls):
        return cls.__name__

    def __repr__(cls):
        n = len(cls.metakernels)
        if n == 0:
            s = f'No metakernels available. Please Update your list: `{cls}.update()`.'
        else:
            s = '\n - '.join([
                f'{n} metakernel' + ('s are ' if n > 1 else ' is ') + 'available:',
                *sorted(cls.metakernels.keys(), reverse=True)
            ])

        return f'<{cls.__class__.__name__}> {s}'

    def __len__(cls):
        return len(cls.metakernels)

    def __iter__(cls):
        return iter(cls.metakernels.values())

    def __contains__(cls, other):
        return str(other) in cls.metakernels.keys()

    def __getitem__(cls, key):
        return cls.get(key)

    def __delitem__(cls, key):
        cls.remove(key)

    @property
    def __dict__(cls):
        return cls.__class__.__dict__

    @property
    def metakernels(cls) -> dict:
        """Dict of available metakernels."""
        if not cls.__mk:
            cls.load_cache()
        return cls.__mk

    def load_cache(cls):
        """Load CReMA metakernel list from the cached CSV file.

        Note
        ----
        If no CReMA cache is available locally, the list will be
        fetch from ESA website with the :py:func:`update` method.

        """
        cremas = cls.read_cache()

        if cremas:
            for crema in cremas:
                cls.add(*crema, cache=False)
        else:
            cls.update()

    def add(cls, key, desc=None, changes=None, metakernel=None, cache=True,
            force_download=False):
        """Add CReMA metakernel.

        Parameters
        ----------
        key: str
            CReMA key (used as a key).
        desc: str, optional
            CReMA description/overview.
        changes: str, optional
            CReMA changes/main update.
        metakernel: str or pathlib.Path
            CReMA remote or local location.
        cache: bool, optional
            Save the kernel information in a cached csv file.
        force_download: bool, optional
            Force file download even if the file is cached
            or availabe locally.

        Note
        ----
        If the :py:obj:`CReMAMetaKernel` is already present
        it will be updated.

        """
        # Create MetaKernel object
        meta = CReMAMetaKernel(key, desc=desc, changes=changes, metakernel=metakernel,
                               force_download=force_download)

        # Append/Update metakernels list
        cls.__mk[str(meta)] = meta

        # Cache the data
        if cache:
            cls.save_cache()

    def get(cls, key):
        """Get CReMA metakernel.

        Parameters
        ----------
        key: str
            CReMA key (used as a key).

        Returns
        -------
        CReMAMetaKernel
            Requested metakernel.

        Raises
        ------
        KeyError
            If the key is invalid.

        """
        # Check if the key is valid
        if str(key) not in cls:
            raise KeyError(f'Unknown {cls} `{key}`')

        return cls.metakernels[str(key)]

    def remove(cls, key, cache=True, delete_file=False):
        """Remove CReMA metakernel.

        Parameters
        ----------
        key: str
            CReMA key (used as a key).
        cache: bool, optional
            Remove the kernel information from the cached csv file.
        delete_file: bool, optional
            Remove the metakernel file (default: ``False``).

        Raises
        ------
        KeyError
            If the key is invalid.

        """
        # Check if key exist
        if str(key) not in cls:
            raise KeyError(f'Unknown {cls} `{key}`')

        # if requested delete the metakernel file
        if delete_file:
            cls[key].fname.unlink()

        # Remove from metakernels list
        del cls.__mk[str(key)]

        # Remove from the cache
        if cache:
            cls.save_cache()

    def read_cache(cls):
        """Load CReMA cached list."""
        if cls.CSV is None or not cls.CSV.exists():
            return []

        lines = cls.CSV.read_text(encoding='utf-8').splitlines()

        return [line.split(', ') for line in lines if not line.startswith('#')]

    def save_cache(cls):
        """Save cache in csv file."""
        if cls.CSV is not None:
            cls.CSV.write_text(
                '\n'.join([
                    '# CReMA, desc, changes, metakernel',
                    *[crema.csv for crema in cls]
                ])
            )

    def update(cls):
        """Download and update CReMA list.

        The list of CReMA is cached internally.

        """
        for crema in cls.get_data():
            cls.add(*crema, cache=False, force_download=True)

        cls.save_cache()

    def get_data(cls):
        """Get CReMA list from ESA website.

        Returns
        -------
        [CReMAMetaKernel, …]
            List of CReMA meta-kernels from ESA website.

        Raises
        ------
        ValueError
            If the parsed data from ESA website is invalid.

        """
        log_esa_crema.info('Downloading the latest list of CReMA from ESA website...')

        # Download the data
        with urlopen(cls.URL) as resp:
            encoder = resp.headers.get_content_charset('utf-8')
            content = resp.read().decode(encoder)
            content = content.replace('&nbsp;', '')
            content = content.replace('\u200b', '')  # Remove zero width space characters
            content = content.replace(',', ';')  # Remove commas
            content = ' '.join((content.split()))    # Strip lines

        log_esa_crema.debug('Download complete.')

        # Parse the data
        parser = CReMAParser()
        parser.feed(content)

        # Split the header and the data
        header, *cremas = parser.data

        parser.close()

        log_esa_crema.debug('Parsing complete.')

        # Check header validity
        if header != ('CReMA', 'Overview', 'Main Update', 'Metakernel'):
            raise ValueError(f'Invalid table header: `{header}`')  # pragma: no cover

        return cremas

    def purge(cls):
        """Remove all cached metakernels."""
        for meta in cls.CSV.parent.glob('*.tm'):
            meta.unlink()

        cls.CSV.unlink()
        cls.__mk = {}


class CReMAMetaKernel(MetaKernel):
    """CReMA Meta-kernel object.

    Parameters
    ----------
    key: str
        CReMA key (used as a key).
    desc: str, optional
        CReMA description/overview.
    changes: str, optional
        CReMA changes/main update.
    metakernel: str or pathlib.Path
        CReMA remote or local location.
    force_download: bool, optional
        Force download even if the file is
        cached or available locally
        (default: `False`)

    Raises
    ------
    AttributeError
        If no metakernel is supplied.

    Note
    ----
    If the :py:attr:`metakernel` is provided as a remote url
    (ie. containing ``://``), the file will be automatically downloaded
    and cached locally.

    """

    def __init__(self, key, desc=None, changes=None, metakernel=None,
                 force_download=False):
        if metakernel is None:
            raise AttributeError('Metakernel location is mandatory.')

        self.key = key
        self.desc = desc
        self.changes = changes
        self.metakernel = str(metakernel)

        fname = Path(self.metakernel)

        # If remote, download the file if not present locally
        if '://' in self.metakernel:
            fname = DATA / fname.name

            if not fname.exists() or force_download:
                wget(self.metakernel, fname, force=force_download)

        super().__init__(fname)

    def __str__(self):
        return self.key

    def __repr__(self):
        s = f'<{self.__class__.__name__}> {self}'
        if self.desc:
            s += f' -- {self.desc}'
        if self.changes:
            s += '\n - '
            s += '\n - '.join(self.changes.split('|'))
        return s

    def __eq__(self, other):
        return str(self) == other

    @property
    def description(self):
        """CReMA description."""
        return self.desc

    @property
    def overview(self):
        """Alias for the CReMA description."""
        return self.desc

    @property
    def main_update(self):
        """Alias for the CReMA changes."""
        return self.changes

    @property
    def csv(self):
        """Row representation in CSV export."""
        return ', '.join([
            self.key,
            self.desc,
            self.changes,
            self.metakernel,
        ])


class CReMAParser(HTMLParser):
    """CReMA HTML table parser."""
    def __init__(self):
        super().__init__()

        self.table = False
        self.tr = False
        self.td = False
        self.ul = False
        self.li = False
        self.a = False

        self._row = []
        self._ul = []
        self._li = []
        self._href = None
        self.data = []

    def error(self, message):
        raise NotImplementedError

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.table = True
        elif self.table and tag == 'tr':
            self.tr = True
        elif self.tr and tag == 'td':
            self.td = True
        elif self.td and tag == 'ul':
            self.ul = True
        elif self.ul and tag == 'li':
            self.li = True
        elif self.td and tag == 'a':
            self.a = True
            for key, value in attrs:
                if key == 'href':
                    self._row.append(value)

    def handle_endtag(self, tag):
        if tag == 'table':
            self.table = False
        elif self.table and tag == 'tr':
            self.tr = False
            self.data.append(tuple(self._row))
            self._row = []
        elif self.tr and tag == 'td':
            self.td = False
        elif self.td and tag == 'ul':
            self.ul = False
            self._row.append('|'.join(self._ul))
            self._ul = []
        elif self.ul and tag == 'li':
            self.li = False
            self._ul.append(' '.join(self._li))
            self._li = []
        elif self.td and tag == 'a':
            self.a = False

    def handle_data(self, data):
        if self.td and data != ' ':
            if self.li:
                self._li.append(data)
            elif not self.a:
                self._row.append(data)
