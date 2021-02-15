from poisson_approval.constants.basic_constants import *
from poisson_approval.iterables.IterableSimplexGrid import IterableSimplexGrid
from poisson_approval.profiles.ProfileHistogram import ProfileHistogram


class IterableProfileHistogramGrid:
    """Iterate over histogram profile (:class:`ProfileHistogram`) defined on a grid.

    Parameters
    ----------
    denominator : int or iterable
        The grain(s) of the grid.
    types : iterable
        These types will have a variable share. They must eih=ther give a ranking and a histogram, e.g.
        ``('abc', (0.2, 0.1, 0.4, 0.3))``, or be a weak order, e.g. ``'a~b>c'``.
    d_type_fixed_share : dict, optional
        A dictionary. For each entry ``type: fixed_share``, this type will have at least this fixed share. The total
        must be lower or equal to 1.
    standardized : bool, optional
        If True, then only standardized profiles are given. Cf. :meth:`Profile.is_standardized`. You should
        probably use this option if the arguments `types`, `d_type_fixed_share` and `test` treat the candidates
        symmetrically.
    test : callable, optional
        A function ``ProfileHistogram -> bool``. Only profiles meeting this test are given.
    kwargs
        Additional parameters are passed to :class:`ProfileHistogram` when creating the profile.

    Examples
    --------
    Basic usage:

        >>> for profile in IterableProfileHistogramGrid(denominator=3, types=[('abc', (0.3, 0.7)), 'a~b>c']):
        ...     print(profile)
        <abc: 1 [0.3 0.7]> (Condorcet winner: a)
        <abc: 2/3 [0.3 0.7], a~b>c: 1/3> (Condorcet winner: a)
        <abc: 1/3 [0.3 0.7], a~b>c: 2/3> (Condorcet winner: a)
        <a~b>c: 1> (Condorcet winner: a, b)

    For more examples, cf. :class:`IterableSimplexGrid`.
    """
    def __init__(self, denominator, types, d_type_fixed_share=None, standardized=False, test=None, **kwargs):
        self.standardized = standardized
        self._base_iterator = IterableSimplexGrid(cls=ProfileHistogram, denominator=denominator, keys=types,
                                                  d_key_fixed_share=d_type_fixed_share, test=test, **kwargs)

    def __iter__(self):
        return (profile for profile in self._base_iterator
                if not self.standardized or profile.is_standardized)
