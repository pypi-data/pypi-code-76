from __future__ import annotations
from logger import logger
from .common import Interval
from ..constants import int_types
from ..check_utils import check_value, check_type, check_type_from_list

class BGR:
    def __init__(self, b: int, g: int, r: int):
        check_type_from_list(item_list=[b, g, r], valid_type_list=int_types)
        self.b = b
        self.g = g
        self.r = r

    def __str__(self):
        return f"BGR({self.b},{self.g},{self.r})"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other: BGR) -> BGR:
        b, g, r = self.b + other.b, self.g + other.g, self.r + other.r
        b, g, r = 255 if b > 255 else b, 255 if g > 255 else g, 255 if r > 255 else r
        return BGR(b=b, g=g, r=r)

    def __sub__(self, other: BGR) -> BGR:
        b, g, r = self.b - other.b, self.g - other.g, self.r - other.r
        b, g, r = 0 if b < 0 else b, 0 if g < 0 else g, 0 if r < 0 else r
        return BGR(b=b, g=g, r=r)

    def __lt__(self, other: BGR) -> bool:
        return self.b < other.b and self.g < other.g and self.r < other.r

    def __gt__(self, other: BGR) -> bool:
        return self.b > other.b and self.g > other.g and self.r > other.r

    def __le__(self, other: BGR) -> bool:
        return self.b <= other.b and self.g <= other.g and self.r <= other.r

    def __ge__(self, other: BGR) -> bool:
        return self.b >= other.b and self.g >= other.g and self.r >= other.r

    def __eq__(self, other: BGR) -> bool:
        return self.b == other.b and self.g == other.g and self.r == other.r

    def __ne__(self, other: BGR) -> bool:
        return self.b != other.b or self.g != other.g or self.r != other.r

    def copy(self) -> BGR:
        return BGR(b=self.b, g=self.g, r=self.r)

    def to_list(self) -> list:
        return [self.b, self.g, self.r]

    @classmethod
    def from_list(self, val_list: list) -> BGR:
        b, g, r = val_list
        return BGR(b=b, g=g, r=r)

class BGR_Interval:
    def __init__(self, b_interval: Interval, g_interval: Interval, r_interval: Interval):
        self.b_interval = b_interval
        self.g_interval = g_interval
        self.r_interval = r_interval

    def __str__(self):
        bgr_lower, bgr_higher = self.to_bgr_pair()
        return f"BGR_Interval({bgr_lower}, {bgr_higher})"

    def __repr__(self):
        return self.__str__()

    def copy(self) -> BGR_Interval:
        return BGR_Interval(
            b_interval=self.b_interval.copy(),
            g_interval=self.g_interval.copy(),
            r_interval=self.r_interval.copy()
        )

    def to_interval_list(self) -> list:
        return [self.b_interval, self.g_interval, self.r_interval]

    def to_list(self) -> list:
        return [interval.to_list() for interval in self.to_interval_list()]

    def to_bgr_pair(self) -> (BGR, BGR):
        b_lower, b_higher = self.b_interval.to_list()
        g_lower, g_higher = self.g_interval.to_list()
        r_lower, r_higher = self.r_interval.to_list()
        bgr_lower = BGR(b=b_lower, g=g_lower, r=r_lower)
        bgr_higher = BGR(b=b_higher, g=g_higher, r=r_higher)
        return bgr_lower, bgr_higher

    def get_lower(self) -> BGR:
        bgr_lower, bgr_higher = self.to_bgr_pair()
        return bgr_lower

    def get_higher(self) -> BGR:
        bgr_lower, bgr_higher = self.to_bgr_pair()
        return bgr_higher

    def contains(self, bgr: BGR, bound_type: str='closed') -> bool:
        """
        bound_type
            'closed': Include boundary values
            'open': Exclude boundary values
        """
        check_type(item=bgr, valid_type_list=[BGR])
        check_value(item=bound_type.lower(), valid_value_list=['closed', 'open'])
        bgr_lower, bgr_upper = self.to_bgr_pair()
        if bound_type.lower() == 'closed':
            return bgr_lower <= bgr and bgr <= bgr_upper
        elif bound_type.lower() == 'open':
            return bgr_lower < bgr and bgr < bgr_upper
        else:
            raise Exception

    def contains_detailed(self, bgr: BGR, bound_type: str='closed') -> list:
        """
        bound_type
            'closed': Include boundary values
            'open': Exclude boundary values
        """
        check_type(item=bgr, valid_type_list=[BGR])
        check_value(item=bound_type.lower(), valid_value_list=['closed', 'open'])
        bgr_lower, bgr_upper = self.to_bgr_pair()
        if bound_type.lower() == 'closed':
            return [
                val_lower <= val and val <= val_upper for val, val_lower, val_upper in \
                    zip(bgr.to_list(), bgr_lower.to_list(), bgr_upper.to_list())
            ]
        elif bound_type.lower() == 'open':
            return [
                val_lower < val and val < val_upper for val, val_lower, val_upper in \
                    zip(bgr.to_list(), bgr_lower.to_list(), bgr_upper.to_list())
            ]
        else:
            raise Exception

    def contains_bgr_interval(self, bgr_interval: BGR_Interval, bound_type: str='closed') -> bool:
        """
        bound_type
            'closed': Include boundary values
            'open': Exclude boundary values
        """
        if self.contains(bgr=bgr_interval.get_lower(), bound_type=bound_type) and \
            self.contains(bgr=bgr_interval.get_higher(), bound_type=bound_type):
            return True
        else:
            return False

    def contains_bgr_interval_detailed(self, bgr_interval: BGR_Interval, bound_type: str='closed') -> bool:
        """
        bound_type
            'closed': Include boundary values
            'open': Exclude boundary values
        """
        lower_contained_list = self.contains_detailed(bgr=bgr_interval.get_lower(), bound_type=bound_type)
        higher_contained_list = self.contains_detailed(bgr=bgr_interval.get_higher(), bound_type=bound_type)
        return [
            lower_contained and higher_contained for lower_contained, higher_contained in \
                zip(lower_contained_list, higher_contained_list)
        ]

    def has_boundary(self, bgr: BGR) -> (bool, str):
        """
        ---output---
        return on_boundary, side

        on_boundary
            Whether or not val is equal to min_val or max_val

        side
            If on_boundary, val == min_val -> 'left'
            If not on_boundary, val == max_val -> 'right'
        """
        on_boundary = False
        side = None
        if bgr == self.get_lower():
            side = 'left'
            on_boundary = True
        elif bgr == self.get_higher():
            side = 'right'
            on_boundary = True
        return on_boundary, side

    def split_at(self, bgr: BGR, inclusive_side: str=None) -> (BGR_Interval, BGR_Interval):
        def split_channel(interval: Interval, val: int) -> (Interval, Interval):
            if interval.contains(val):
                left, right = interval.split_at(val, inclusive_side=inclusive_side)
            else:
                left, right = interval, None
            return left, right

        b_left, b_right = split_channel(interval=self.b_interval, val=bgr.b)
        g_left, g_right = split_channel(interval=self.g_interval, val=bgr.g)
        r_left, r_right = split_channel(interval=self.r_interval, val=bgr.r)

        if b_left is None and g_left is None and r_left is None: # Failed to resolve
            bgr_left = None
        else:
            b_left = b_right if b_left is None else b_left
            g_left = g_right if g_left is None else g_left
            r_left = r_right if r_left is None else r_left
            bgr_left = BGR_Interval(b_interval=b_left, g_interval=g_left, r_interval=r_left)
        if b_right is None and g_right is None and r_right is None: # Failed to resolve
            bgr_right = None
        else:
            b_right = b_left if b_right is None else b_right
            g_right = g_left if g_right is None else g_right
            r_right = r_left if r_right is None else r_right
            bgr_right = BGR_Interval(b_interval=b_right, g_interval=g_right, r_interval=r_right)
        return bgr_left, bgr_right

    def intersects(self, bgr_interval: BGR_Interval, bound_type: str='open') -> (bool, bool, bool):
        return [
            host_interval.intersects(target_interval, bound_type=bound_type) for host_interval, target_interval in \
                zip(self.to_interval_list(), bgr_interval.to_interval_list())
        ]

    def intersect(self, bgr_interval: BGR_Interval) -> list:
        result = []
        for host_interval, target_interval in \
            zip(self.to_interval_list(), bgr_interval.to_interval_list()):
            if not host_interval.intersects(target_interval, bound_type='closed'):
                result.append(None)
            else:
                result.append(host_interval.intersect(target_interval))

        return result

    def union(self, bgr_interval: BGR_Interval) -> list:
        result = []
        for host_interval, target_interval in \
            zip(self.to_interval_list(), bgr_interval.to_interval_list()):
            if not host_interval.intersects(target_interval, bound_type='closed'):
                result.append(None)
            else:
                result.append(host_interval.union(target_interval))

        return result

    def exclude_interval(self, bgr_interval: BGR_Interval) -> (BGR_Interval, BGR_Interval):
        raise NotImplementedError
        [b_interval, g_interval, r_interval] = self.intersect(bgr_interval.copy())
        b_interval = b_interval if b_interval is not None else bgr_interval.b_interval
        g_interval = g_interval if g_interval is not None else bgr_interval.g_interval
        r_interval = r_interval if r_interval is not None else bgr_interval.r_interval
        working_bgr_interval = BGR_Interval.from_interval_list([b_interval, g_interval, r_interval])

        logger.red(working_bgr_interval)

        part0, temp0 = self.split_at(working_bgr_interval.get_lower())
        # logger.red(temp0)
        temp1, part1 = temp0.split_at(working_bgr_interval.get_higher())
        return part0, part1

    @classmethod
    def from_interval_list(self, bgr_interval_list: list) -> BGR_Interval:
        b_interval, g_interval, r_interval = bgr_interval_list
        return BGR_Interval(b_interval=b_interval, g_interval=g_interval, r_interval=r_interval)

    @classmethod
    def from_list(self, bgr_list: list) -> BGR_Interval:
        b_interval_list, g_interval_list, r_interval_list = bgr_list
        b_interval = Interval.from_list(b_interval_list)
        g_interval = Interval.from_list(g_interval_list)
        r_interval = Interval.from_list(r_interval_list)
        return BGR_Interval.from_interval_list([b_interval, g_interval, r_interval])

    @classmethod
    def from_bgr_pair(self, bgr_lower: BGR, bgr_higher: BGR) -> BGR_Interval:
        b_lower, g_lower, r_lower = bgr_lower.to_list()
        b_higher, g_higher, r_higher = bgr_higher.to_list()
        b_interval = Interval(b_lower, b_higher)
        g_interval = Interval(g_lower, g_higher)
        r_interval = Interval(r_lower, r_higher)
        return BGR_Interval(b_interval, g_interval, r_interval)

    @classmethod
    def test(self):
        bgr0 = BGR(50, 25, 99)
        bgr1 = BGR(50, 200, 99)

        bgr_interval = BGR_Interval.from_bgr_pair(BGR(0, 0, 0), BGR(100, 100, 100))
        bgr_interval0 = BGR_Interval.from_bgr_pair(BGR(25, 25, 25), BGR(50, 50, 50))
        bgr_interval1 = BGR_Interval.from_bgr_pair(BGR(25, 25, 25), BGR(50, 125, 50))
        left_bgr_interval, right_bgr_interval = bgr_interval.split_at(bgr=bgr0)

        logger.cyan(f"bgr_interval: {bgr_interval}")
        logger.cyan(f"Split at {bgr0}")
        logger.yellow(f"Result: {left_bgr_interval}, {right_bgr_interval}")
        logger.yellow(f"bgr_interval.contains({bgr0}): {bgr_interval.contains(bgr0)}")
        logger.yellow(f"bgr_interval.contains({bgr1}): {bgr_interval.contains(bgr1)}")
        logger.yellow(f"bgr_interval.contains_detailed({bgr1}): {bgr_interval.contains_detailed(bgr1)}")
        logger.yellow(f"bgr_interval.contains_bgr_interval(left_bgr_interval): {bgr_interval.contains_bgr_interval(left_bgr_interval)}")
        logger.yellow(f"bgr_interval.contains_bgr_interval(right_bgr_interval): {bgr_interval.contains_bgr_interval(right_bgr_interval)}")
        logger.purple(f"bgr_interval.contains_bgr_interval_detailed(bgr_interval0): {bgr_interval.contains_bgr_interval_detailed(bgr_interval0)}")
        logger.purple(f"bgr_interval.contains_bgr_interval_detailed(bgr_interval1): {bgr_interval.contains_bgr_interval_detailed(bgr_interval1)}")

        # logger.blue(f"bgr_interval.exclude_interval(bgr_interval0): {bgr_interval.exclude_interval(bgr_interval0)}")
        # logger.blue(f"bgr_interval.exclude_interval(bgr_interval1): {bgr_interval.exclude_interval(bgr_interval1)}")
