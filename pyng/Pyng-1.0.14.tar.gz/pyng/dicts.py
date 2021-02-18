#!/usr/bin/python
"""
    dicts.py                         Nat Goodspeed
    Copyright (C) 2016               Nat Goodspeed

NRG 2016-03-01
"""

from past.builtins import basestring
import collections

# ****************************************************************************
#   Dictionary augmentation
# ****************************************************************************
class addict(dict):
    """
    addict isa dict with the additional property that you can use the +
    operator with dict and addict (in either order) to obtain a dict with the
    set union of keys. This operation is NOT commutative: any key found in
    both the left and the right dict is overwritten by the value in the right
    dict, as with dict.update(). Given two dicts a and b, a + b is equivalent
    to a.update(b), save for three things:

    * a and b remain unmodified
    * a + b returns the result, unlike update()
    * a + b returns an addict, permitting a + b + ... chaining with additional
      dicts or addicts
    """
    def __init__(self, *args, **kwds):
        """
        addict can also be used as a function. If a, b and c are dicts,
        addict(a, b, c) produces an addict containing a + b + c. As with
        dict's constructor, addict(a, b, c, key=value, ...) overrides any
        previous 'key' in a, b or c.
        """
        # Forward a single dict (or sequence) positional argument, if present,
        # to base-class constructor. Don't forward keyword arguments yet.
        super(addict, self).__init__(*args[:1])
        # update() ourself with each additional positional argument
        for add in args[1:]:
            self.update(add)
        # finally, apply keyword overrides
        self.update(kwds)

    def copy(self):
        """
        Override copy() to return another addict, rather than plain dict
        """
        return self.__class__(self)

    def __add__(self, other):
        """
        addict + dict
        """
        new = self.copy()
        new.update(other)
        return new

    def __radd__(self, other):
        """
        dict + addict
        """
        # This is a bit tricky, in that if 'other' is a plain dict,
        # other.copy() would return a plain dict, which would prohibit
        # chaining a + b + c operations. So explicitly copy 'other' to an
        # addict first.
        new = self.__class__(other)
        new.update(self)
        return new

    # Since we support +, why not - also? In this case 'other' can be any
    # iterable of keys. Happily, a dict can be treated as an iterable of keys.
    def __sub__(self, other):
        """
        addict - dict
        """
        return subdict(self, set(self).difference(other))

    def __rsub__(self, other):
        """
        dict - addict
        """
        return subdict(other, set(other).difference(self))

# ****************************************************************************
#   Dictionary subsets
# ****************************************************************************
def subdict(d, keys):
    """
    Subset of a dict, specified by an iterable of desired keys. If a
    specified key isn't found, you get a KeyError exception. Use interdict()
    if you want softer failure.
    """
    # Since we're constructing a new dict anyway, might as well make it an
    # addict; this supports addict.__sub__() and __rsub__() chaining without
    # penalizing other uses.
    return addict([(key, d[key]) for key in keys])

def interdict(d, keys):
    """
    Set intersection of a dict and an iterable of desired keys. Ignores any
    key in 'keys' not already present in the dict. Use subdict() if you'd
    prefer a KeyError.
    """
    # Guessing that the builtin set intersection operation is more efficient
    # than explicit Python membership tests.
    return subdict(d, set(d).intersection(keys))

# ****************************************************************************
#   smartdefaultdict
# ****************************************************************************
class smartdefaultdict(collections.defaultdict):
    """
    Like defaultdict, but the default_factory callable you pass the
    constructor must accept the (missing) key as argument. As with
    defaultdict, the value returned by default_factory(key) becomes the value
    of smartdefaultdict[key].

    smartdefaultdict can be used to implement 'Mostly I want to call such-and-
    such idempotent function f(x), except for a specific value of x whose
    result should be y.' Instantiate
    d = smartdefaultdict(f, x0=y0, x1=y1, ...)
    and then d[x] gives you that behavior. Bonus: prior results are cached, in
    case f(x) is at all expensive.
    """
    # "smartdefaultdict" seems more succinct (and easier to remember) than
    # "knowingdefaultdict" or "defaultdictwithkey" or the like.
    def __missing__(self, key):
        # When you instantiate a defaultdict with a default_factory callable,
        # and try to retrieve a nonexistent key, your default_factory callable
        # is called with no arguments. It does not know the key you were
        # trying to retrieve. For cases when that's insufficient, override
        # __missing__() to pass the missing key to default_factory. (That
        # would've made a better design for defaultdict in the first place,
        # but oh well, it's not that hard to achieve.)
        return self.default_factory(key)

# ****************************************************************************
#   dict search
# ****************************************************************************
def preddict(d, pred, _idxs=()):
    """
    Given a data structure of arbitrary depth -- scalar, iterable, associative
    -- any element of which might be another container -- search for elements
    for which 'pred' (a callable accepting an entry) returns True.

    This function is a generator which will eventually traverse the whole
    structure in depth-first order. It DOES NOT DEFEND against circularity.

    Every time pred(element) returns True, yield a tuple that can be used to
    navigate the data structure back to the found element. The tuple is
    constructed as follows:

    Each element of the tuple steps down to the next level of the data
    structure.

    If the current level of the data structure is a dict, the corresponding
    tuple element is the dict key.

    If the current level of the data structure is a list or tuple, the
    corresponding tuple element is the int index.

    If the entire data structure is a scalar for which pred(d) returns True,
    the tuple will be empty.

    Thus, a loop like this:

    element = d
    for t in yielded_tuple:
        element = element[t]

    should make pred(element) return True.
    """
    if isinstance(d, collections.Mapping):
        for k, v in d.items():
            for tup in preddict(v, pred, _idxs + (k,)):
                yield tup
    elif isinstance(d, collections.Sequence) \
    and not isinstance(d, basestring):
        # This clause is for list, tuple etc. -- NOT strings.
        for i, v in enumerate(d):
            for tup in preddict(v, pred, _idxs + (i,)):
                yield tup
    else:
        # scalar, we hope! or string.
        try:
            # Test this value by calling the passed predicate.
            found = pred(d)
        except (TypeError, AttributeError):
            # Explicitly allow predicates that might not be suitable for all
            # datatypes. For instance, we want to be able to search for all
            # strings containing some substring using the 'in' operator even
            # if not all elements in the data structure are strings.
            pass
        else:
            # pred(d) didn't raise an exception -- did it return True?
            if found:
                yield _idxs

def all_eq_in_dict(d, value):
    """
    Given a data structure of arbitrary depth as described for preddict(),
    generate an index tuple for each element equal to the passed value.
    """
    return preddict(d, lambda v: v == value)

def first_eq_in_dict(d, value):
    """
    Given a data structure of arbitrary depth as described for preddict(),
    return the index tuple for the first element equal to the passed value, or
    None. (Be careful to distinguish None from the empty tuple (). The latter
    is returned when 'd' is a scalar equal to 'value'.)
    """
    try:
        # Obtain the generator-iterator returned by all_in_dict(), then get
        # the first value.
        return next(all_eq_in_dict(d, value))
    except StopIteration:
        # all_eq_in_dict() traversed the whole structure without yielding
        # anything.
        return None
