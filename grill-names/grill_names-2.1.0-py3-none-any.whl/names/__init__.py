from __future__ import annotations
import typing
from datetime import datetime

import naming
from grill.tokens import ids


def _table_from_id(id_mapping):
    headers = [
        'Token',
        'Pattern',
        'Default',
        'Description',
    ]
    table_sep = tuple([''] * len(headers))
    sorter = lambda m: (
        # cleanup backslashes formatting
        m["pattern"].replace('\\', '\\\\'),
        m['default'],
        # replace new lines with empty strings to avoid malformed tables.
        m['description'].replace('\n', ' '),
    )
    rows = [table_sep, headers, table_sep]
    rows.extend([token, *sorter(values)] for token, values in id_mapping.items())
    rows.append(table_sep)
    max_sizes = [(max(len(i) for i in r)) for r in zip(*rows)]

    format_rows = []
    for r in rows:
        filler = '=<' if r == table_sep else ''
        format_rows.append(' '.join(
            f"{{:{f'{filler}'}{f'{size}'}}}".format(i)
            for size, i in zip(max_sizes, r))
        )
    return '\n'.join(format_rows)


class DefaultName(naming.Name):
    """ Inherited by: :class:`grill.names.CGAsset` :class:`grill.names.DateTimeFile`

    Base class for any Name object that wishes to provide `default` functionality via
    the `get_default` method.

    Subclass implementations can override the `_defaults` member to return a mapping
    appropriate to that class.
    """
    _defaults = {}

    @classmethod
    def get_default(cls, **kwargs) -> DefaultName:
        """Get a new Name object with default values and overrides from **kwargs."""
        name = cls()
        defaults = dict(name._defaults, **kwargs)
        name.name = name.get(**defaults)
        return name


class DateTimeFile(naming.File, DefaultName):
    """Time based file names respecting iso standard.

    ============= ================
    **Config:**
    ------------------------------
    *year*        Between :py:data:`datetime.MINYEAR` and :py:data:`datetime.MAXYEAR` inclusive.
    *month*       Between 1 and 12 inclusive.
    *day*         Between 1 and the number of days in the given month of the given year.
    *hour*        In ``range(24)``.
    *minute*      In ``range(60)``.
    *second*      In ``range(60)``.
    *microsecond* In ``range(1000000)``.
    ============= ================

    ======  ============
    **Composed Fields:**
    --------------------
    *date*  `year` `month` `day`
    *time*  `hour` `minute` `second` `microsecond`
    ======  ============

    .. note::
        When getting a new default name, current ISO time at the moment of execution is used.

    Example:
        >>> tf = DateTimeFile.get_default(suffix='txt')
        >>> tf.day
        '28'
        >>> tf.date
        '2019-10-28'
        >>> tf.year = 1999
        >>> tf
        DateTimeFile("1999-10-28 22-29-31-926548.txt")
        >>> tf.month = 14  # ISO format validation
        Traceback (most recent call last):
            ...
        ValueError: month must be in 1..12
        >>> tf.datetime
        datetime.datetime(1999, 10, 28, 22, 29, 31, 926548)
    """

    config = dict.fromkeys(
        ('month', 'day', 'hour', 'minute', 'second'), r'\d{1,2}'
    )
    config.update(year=r'\d{1,4}', microsecond=r'\d{1,6}')
    join = dict(
        date=('year', 'month', 'day'),
        time=('hour', 'minute', 'second', 'microsecond'),
    )
    join_sep = '-'

    @property
    def _defaults(self):
        time_field = {'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'}
        now = datetime.now()
        return dict(
            {f: getattr(now, f) for f in time_field},
            suffix='ext',
        )

    def get_pattern_list(self) -> typing.List[str]:
        """Fields / properties names (sorted) to be used when building names.

        Defaults to [`date`, `time`] + keys of this name's config
        """
        return ["date", "time"] + list(self.config)

    @property
    def name(self) -> str:
        return super().name

    @name.setter
    def name(self, name: str):
        prev_name = self._name
        super(DateTimeFile, self.__class__).name.fset(self, name)
        if name:
            try:  # validate via datetime conversion
                self.datetime
            except ValueError:
                if prev_name:  # if we had a previous valid name, revert to it
                    self.name = prev_name
                raise

    @property
    def datetime(self) -> datetime:
        """ Return a :py:class:`datetime.datetime` object using this name values.

            >>> tf = DateTimeFile("1999-10-28 22-29-31-926548.txt")
            >>> tf.datetime
            datetime.datetime(1999, 10, 28, 22, 29, 31, 926548)
        """
        if not self.name:
            raise AttributeError("Can not retrieve datetime from an empty name")
        date = f"{int(self.year):04d}-{int(self.month):02d}-{int(self.day):02d}"
        time = (f"{int(self.hour):02d}:{int(self.minute):02d}:{int(self.second):02d}."
                f"{int(self.microsecond):06d}")
        return datetime.fromisoformat(f'{date}T{time}')


class CGAsset(DefaultName):
    """Inherited by: :class:`grill.names.CGAssetFile`

    Elemental resources that, when composed, generate the entities that bring an idea to a tangible product
    through their life cycles (e.g. a character, a film, a videogame).

    """
    config = {k: v['pattern'] for k, v in ids.CGAsset.items()}
    __doc__ += '\n' + _table_from_id(ids.CGAsset) + '\n'

    def __init__(self, *args, sep='-', **kwargs):
        super().__init__(*args, sep=sep, **kwargs)

    @property
    def _defaults(self):
        return {k: v['default'] for k, v in ids.CGAsset.items()}


class CGAssetFile(CGAsset, naming.PipeFile):
    """Versioned files in the pipeline for a CGAsset.

    Example:
        >>> name = CGAssetFile.get_default(version=7)
        >>> name.suffix
        'ext'
        >>> name.suffix = 'abc'
        >>> name.path
        WindowsPath('demo/3d/abc/entity/rnd/lead/atom/main/all/whole/7/demo-3d-abc-entity-rnd-lead-atom-main-all-whole.7.abc')
    """

    @property
    def _defaults(self):
        result = super()._defaults
        result.update(version=1, suffix='ext')
        return result

    def get_path_pattern_list(self) -> typing.List[str]:
        pattern = super().get_pattern_list()
        pattern.append('version')
        return pattern


class LifeTR(naming.Name):
    """Taxonomic Rank used for biological classification.

    """
    config = {k: v['pattern'] for k, v in ids.LifeTR.items()}
    __doc__ += '\n' + _table_from_id(ids.LifeTR) + '\n'

    def __init__(self, *args, sep=':', **kwargs):
        super().__init__(*args, sep=sep, **kwargs)
