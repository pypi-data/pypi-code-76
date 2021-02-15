"""ExtendedTestCase provides plugin almostEquals and auto-capture of expected results"""

from __future__ import annotations

import inspect
from itertools import islice

from numbers import Number
from typing import Any, Union, Callable, Optional, Tuple, Type, List

from unittest import util
from unittest.case import TestCase
from unittest.util import safe_repr

from x7.testing.support import RecorderError, RecordedData, warn_class, PicklerExtension, Pickler

Matcher = Callable[[Any, Any], Any]
ExplainReturn = Tuple[bool, Optional[str]]

__all__ = [
    'Matcher', 'ExtendedMatcher', 'TestCaseExtended', 'Pickler', 'PicklerExtension',
    'ExtendedMatcherImage',
    'ExplainReturn',
    'RecordedData', 'RecorderError',
]


class ExtendedMatcher:
    """
        ExtendedMatcher does almost_equal comparisons and mismatch explanation,
        providing helpful error messages.
    """

    def __init__(self, test_case: 'TestCaseExtended', kind: Optional[Type] = None):
        """
        :param test_case:   Parent TestCaseExtended class
        :param kind:        type this matcher handles
        """
        self.test_case = test_case
        if kind is None:
            raise ValueError('kind must be supplied by derived classes')
        self.kind = kind

    _nie = NotImplementedError    # Hack to hide (apparently) abstract method from pylint

    def almost_equal(self, first, second, places=None, delta=None) -> Union[bool, str]:
        """Compare first to second.  type(both) will be .type"""
        # Call these for deeper comparisons
        # * self.test_case.almostEqualFloat()   - for floats
        # * self.test_case.almostEqual()        - for other unhandled types
        raise self._nie('almost_equal not implemented for %s' % self.kind.__name__)
        # raise NotImplementedError('almost_equal not implemented for %s' % self.kind.__name__)

    def explain_mismatch(self, new_data, old_data) -> ExplainReturn:
        """
            Explain how new_data differs from old_data

            :param new_data:    New result
            :param old_data:    Expected result
            :return: (Close? and formatted comparison or None for default '%-50s %-50s' % (first, second))
        """
        # * top-level explain only
        raise self._nie('explain_mismatch not implemented for %s' % self.kind.__name__)


class ExtendedMatcherImage(ExtendedMatcher):
    MAX_IMAGE_SIZE = (500, 400)

    def __init__(self, test_case: 'TestCaseExtended'):
        # noinspection PyPackageRequirements
        from PIL import Image, ImageChops
        super().__init__(test_case, Image.Image)
        self.image = Image
        self.image_chops = ImageChops

    def explain_mismatch(self, new_data, old_data) -> ExplainReturn:
        self.show_images(new_data, old_data)
        # TODO-count non-matching pixels?
        return False, 'Images(%r, %s, ...) differ' % (new_data.mode, new_data.size)

    def show_images(self, new_data, old_data):
        # TODO-make a Tk image comparison tool

        if isinstance(new_data, self.image.Image) and isinstance(old_data, self.image.Image):
            if (
                new_data.mode == old_data.mode and
                new_data.size == old_data.size and
                new_data.size < self.MAX_IMAGE_SIZE
            ):
                # Show as a single two-up image for easier comparison
                sx, sy = new_data.size
                im = self.image.new('RGBA', (2 * sx + 30, sy + 20), (128, 128, 128, 255))
                im.paste(new_data, (10, 10, sx + 10, sy + 10))
                im.paste(old_data, (sx + 20, 10, 2 * sx + 20, sy + 10))
                black = (0, 0, 0, 255)
                mid = int(10 + sx / 2)
                for x in range(-3, 4):  # draw N
                    im.putpixel((mid + x, x + 4), black)
                    im.putpixel((mid - 3, x + 4), black)
                    im.putpixel((mid + 3, x + 4), black)
                mid += sx + 10
                for x in range(-2, 3):  # draw O
                    im.putpixel((mid + x, 1), black)
                    im.putpixel((mid + x, 7), black)
                    im.putpixel((mid + 3, x + 4), black)
                    im.putpixel((mid - 3, x + 4), black)
                im.show('new and old')
                diff = self.image_chops.difference(new_data.convert('RGBA'), old_data.convert('RGBA'))
                diff.putalpha(255)
                diff.show('difference')
            else:
                new_data.show('new data')
                old_data.show('old data')
        else:
            raise TypeError('show_images: expected Image, Image; got %s, %s' %
                            (type(new_data).__name__, type(old_data).__name__))


class TestCaseExtended(TestCase):
    # Derived classes should override these values
    PICKLERS: List[Type[PicklerExtension]] = []
    MATCHERS: List[Type[ExtendedMatcher]] = []

    @staticmethod
    def almostEqualFloat(first: float, second: float, places=None, delta=None):
        """Return True if first ~=~ second, else an error message"""
        if first == second:
            # shortcut
            return True
        if delta is not None and places is not None:
            raise TypeError("specify delta or places not both")

        diff = abs(first - second)
        if delta is not None:
            if diff <= delta:
                return True

            msg = '%s != %s within %s delta (%s difference)' % (
                safe_repr(first),
                safe_repr(second),
                safe_repr(delta),
                safe_repr(diff))
        else:
            if places is None:
                places = 7

            if round(diff, places) == 0:
                return True

            msg = '%s != %s within %r places (%.7g difference)' % (
                safe_repr(first),
                safe_repr(second),
                places,
                diff)
        return msg

    @property
    def matchers(self):
        if not hasattr(self, '_matchers'):
            self._matchers = [mc(self) for mc in self.MATCHERS]
        return self._matchers

    @property
    def matchable_types(self):
        return tuple((tuple, ) + tuple(m.kind for m in self.matchers))

    def almostEqual(self, first: Any, second: Any, places: int = None, msg: Any = None, delta: float = None):
        """Return True if first ~=~ second, else an error message"""

        if first == second:
            return True
        if msg is None:
            msg = '%s~=~%s' % (first, second)
        if isinstance(first, (int, float)) and isinstance(second, (int, float)):
            almost = self.almostEqualFloat(first, second, places, delta)
            return almost if almost is True else (msg + ': ' + almost)
        if type(first) != type(second):
            return msg + ': mismatched types: %s vs %s' % (type(first), type(second))

        def msg_idx(i):
            if msg.endswith('] '):
                return msg[:-1] + '[%d] ' % i
            else:
                return msg + '@ [%d] ' % i

        # Any matching extensions?
        for matcher in self.matchers:
            if isinstance(first, matcher.kind):
                return matcher.almost_equal(first, second, places=places, delta=delta)

        if isinstance(first, (list, tuple)) and type(first) is type(second):
            if len(first) != len(second):
                msg += ': mismatched lengths: first=%d  second=%d' % (len(first), len(second))
                return msg
            elif isinstance(first[0], self.matchable_types):       # List of tuples or matchable types
                # Note: we know first is non-empty because:
                #   1. first == second test would catch empty list/tuple
                #   2. len(first) != len(second) would catch []==[...]
                if not isinstance(first[0], type(second[0])):
                    msg += ': mismatched element types: %s vs %s' % (
                        util.strclass(type(first[0])), util.strclass(type(second[0])))
                    return msg
                for idx, (f, s) in enumerate(zip(first, second)):
                    try:
                        self.assertAlmostEqual(f, s, places=places, delta=delta, msg=msg_idx(idx))
                    except self.failureException as err:
                        msg = str(err)      # Use this try/except/raise to simplify traceback stack
                        return msg
                return True
            elif isinstance(first[0], Number):
                for idx, (f, s) in enumerate(zip(first, second)):
                    almost = self.almostEqualFloat(f, s, places=places, delta=delta)
                    if almost is not True:
                        msg = msg_idx(idx)[:-1] + ': ' + almost
                        return msg
                return True
            else:
                return msg + ": almostEqual: don't understand type: %s of %s" % (type(first).__name__, type(first[0]).__name__)

        return msg + ": almostEqual: don't understand type: %s" % type(first).__name__

    def assertAlmostEqual(self, first: Any, second: Any, places: int = None, msg: Any = None, delta: float = None) -> None:
        almost = self.almostEqual(first, second, places, msg, delta)
        if almost is not True:
            if msg is None:
                msg = '%s~=~%s' % (first, second)
            msg = msg + ': ' + almost
            raise self.failureException(msg)

    # class TestCaseRecorder(TestCasePoint):

    # Use 'ignore' to ignore recorder functionality
    # Use True/False to save/not-save new data
    SAVE_MATCH: Union[bool, str] = 'ignore'

    @classmethod
    def setUpClass(cls):
        """Hook method for setting up class fixture before running tests in the class."""
        # print('setupclass:', cls)
        if cls.SAVE_MATCH == 'ignore':
            return

        # pre-load data so that possible warnings come out early
        RecordedData.setup(cls.__module__, Pickler(cls.PICKLERS))
        if cls.SAVE_MATCH:
            warn_class(cls, 'SAVE_MATCH=True, test results being saved, not validated')
        elif RecordedData.get_mod(cls.__module__).new:
            warn_class(cls, 'new .td file, test results being saved, not validated')

    @classmethod
    def tearDownClass(cls):
        if cls.SAVE_MATCH == 'ignore':
            return True

        if cls.SAVE_MATCH or RecordedData.get_mod(cls.__module__).new:
            RecordedData.save_modules()

    def matchExact(self, new_data, old_data) -> Union[bool, str]:
        if new_data == old_data:
            return True
        extra_lines = []
        if type(new_data) is not type(old_data):
            extra_lines.append('mismatched types: %s vs %s' % (type(new_data), type(old_data)))
        elif isinstance(new_data, (list, tuple)):   # Collections to unpack
            if len(new_data) != len(old_data):
                extra_lines.append('length mismatch: new=%d old=%d' % (len(new_data), len(old_data)))
            else:
                worst = 'Match'
                for idx, (n, o) in enumerate(islice(zip(new_data, old_data), 20)):
                    if n == o:
                        status = 'Match'
                    elif type(n) == type(o):
                        # TODO-this was: if isinstance(n, (Point, ControlPoint)):
                        if hasattr(n, 'close'):     # HACK alert.  Needs to be more type-specific
                            if n.close(o):
                                status = 'Close'
                            else:
                                status = 'Diff '
                        else:
                            status = 'Diff '
                    else:
                        status = 'Diff '
                    if status == 'Diff ':
                        worst = status
                    elif worst != 'Diff ' and status == 'Close':
                        worst = status
                    extra_lines.append('[%d]: %s: %-50s %-50s' % (idx, status, n, o))
                use_worst = False
                if use_worst and worst in ('Match', 'Close'):
                    return True
        else:
            # Check for extension
            for matcher in self.matchers:
                if isinstance(new_data, matcher.kind):
                    close, msg = matcher.explain_mismatch(new_data, old_data)
                    if not msg:
                        msg = '%s: %-50s %-50s' % ('Close' if close else 'Diff ', new_data, old_data)
                    extra_lines.append(msg)
                    break

        return '\n'.join(['new_data != old_data: '] + extra_lines + ['%.200r != %.200r' % (new_data, old_data)])

    def match(self, new_data, case='0', func=None, cls=None, matcher: Optional[Matcher] = None):
        """Assert that this run of 'data' matches previous run"""
        matcher: Matcher = matcher or self.matchExact
        if self.SAVE_MATCH == 'ignore':
            raise RecorderError('call to assertMatch when SAVE_MATCH==ignore')
        if cls is None:
            cls = type(self)
        if func is None:
            func = inspect.getframeinfo(inspect.currentframe().f_back.f_back).function
        if self.SAVE_MATCH or RecordedData.get_mod(cls.__module__).new:
            old_data = RecordedData.get(cls, func, case)
            changed = matcher(new_data, old_data) is not True
            if old_data is RecordedData.NONE:
                print('%s.%s:%s: new data' % (cls.__name__, func, case))
            elif changed:
                print('%s.%s:%s: data changed' % (cls.__name__, func, case))
            if changed:
                RecordedData.put(cls, func, case, new_data)
            return True
        else:
            old_data = RecordedData.get(cls, func, case)
            if old_data is RecordedData.NONE:
                msg = '%s.%s:%s: no recorded data' % (type(self).__name__, func, case)
                return msg
            return matcher(new_data, old_data)
            # self.assertEqual(new_data, old_data)

    def match_patch(self, test_data, case='0', func=None, cls=None):
        """
            'patch' some test data into recorded data, does not set changed flag.
            Only used to test infrastructure.
        """
        if self.SAVE_MATCH == 'ignore':
            raise RecorderError('call to match_patch when SAVE_MATCH==ignore')
        if cls is None:
            cls = type(self)
        if func is None:
            func = inspect.getframeinfo(inspect.currentframe().f_back).function
        RecordedData.put(cls, func, case, test_data, True)

    def assertAlmostMatch(self, new_data, case='0', func=None, cls=None):
        msg = self.match(new_data, case, func, cls, lambda f, s: self.almostEqual(f, s))
        if msg is not True:
            raise self.failureException(msg)

    def assertMatch(self, new_data, case='0', func=None, cls=None):
        """.assertMatch, but include full values in error message"""
        def assert_equals(data_new, data_old):
            try:
                self.assertEqual(data_new, data_old)
            except AssertionError as err:
                return err
            return True
        msg = self.match(new_data, case, func, cls, matcher=assert_equals)
        if isinstance(msg, Exception):
            raise msg
        if msg is not True:
            raise self.failureException(msg)
