from __future__ import annotations
import numpy as np
from collections import namedtuple
from logger import logger
from ..check_utils import check_type, check_type_from_list, check_list_length, check_value
from math import pi, asin, tan
from ..constants import number_types, int_types, float_types
from shapely.geometry import Point as ShapelyPoint

Keypoint = namedtuple('Keypoint', ['x', 'y', 'v'])

class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        logger.warning(f"BoundingBox is decapricated. Please use BBox instead.")

class Size:
    _from_list_length = 2
    def __init__(self, width, height, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[width, height], valid_type_list=number_types)
        self.width = width
        self.height = height
        self.area = width * height

    def __str__(self):
        return f"Size: (width, height)=({self.width},{self.height})"

    def __repr__(self):
        return self.__str__()

    def to_int(self):
        return Size(width=int(self.width), height=int(self.height), check_types=False)

    def to_float(self):
        return Size(width=float(self.width), height=float(self.height), check_types=False)

    def to_list(self):
        return [self.width, self.height]

    def items(self) -> list:
        return [self.width, self.height]

    def types(self):
        return [type(self.width), type(self.height)]

    @classmethod
    def from_list(self, items: list):
        check_list_length(item_list=items, correct_length=self._from_list_length)
        return Size(width=items[0], height=items[1])

    @classmethod
    def from_cv2_shape(self, cv2_shape: list):
        h, w = cv2_shape[:2]
        return Size(width=w, height=h)

class Point:
    def __init__(self, x, y, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[x, y], valid_type_list=number_types)
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point: (x, y)=({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def to_int(self):
        return Point(x=int(self.x), y=int(self.y), check_types=False)

    def to_float(self):
        return Point(x=float(self.x), y=float(self.y), check_types=False)

    def to_labelme_format(self):
        return [[self.x, self.y]]

    def to_shapely(self) -> ShapelyPoint:
        return ShapelyPoint(self.to_list())

    def items(self) -> list:
        return [self.x, self.y]

    def to_list(self) -> list:
        return [self.x, self.y]

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def types(self) -> list:
        return [type(self.x), type(self.y)]

    @classmethod
    def from_list(self, items: list):
        check_list_length(item_list=items, correct_length=2)
        return Point(x=items[0], y=items[1])

    @classmethod
    def from_labelme_point_list(self, labelme_point_list: list):
        check_list_length(item_list=labelme_point_list, correct_length=1)
        [[x, y]] = labelme_point_list
        return Point(x, y)

    @classmethod
    def from_shapely(self, shapely_point: ShapelyPoint) -> Point:
        coords = [list(val)[0] for val in shapely_point.coords.xy]
        return Point.from_list(coords)

class Rectangle:
    def __init__(self, xmin, ymin, xmax, ymax, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[xmin, xmax, ymin, ymax], valid_type_list=number_types)
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.width = xmax - xmin
        self.height = ymax - ymin
        self.p0 = Point(x=xmin, y=ymin)
        self.p1 = Point(x=xmax, y=ymax)
        self.area = self.width * self.height
        self.point_list = [self.p0, self.p1]

    def __str__(self):
        return f"Rectangle: (xmin, ymin, xmax, ymax)=({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

    def __repr__(self):
        return self.__str__()

    def to_int(self):
        return Rectangle(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax),
            check_types=False
        )

    def to_float(self):
        return Rectangle(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax),
            check_types=False
        )

    def to_coco_format(self):
        return [self.xmin, self.ymin, self.width, self.height]

    def to_labelme_format(self) -> list:
        return [[self.xmin, self.ymin], [self.xmax, self.ymax]]

    def to_vertex_list(self) -> list:
        """
        Returns vertices in the following order:
        [upper_left, upper_right, lower_right, lower_left]
        """
        return [
            [self.xmin, self.ymin], # upper left
            [self.xmax, self.ymin], # upper right
            [self.xmax, self.ymax], # lower right
            [self.xmin, self.ymax]  # lower left
        ]

    @classmethod
    def from_p0p1(self, p0: Point, p1: Point) -> Point:
        return Rectangle(xmin=p0.x, ymin=p0.y, xmax=p1.x, ymax=p1.y, check_types=False)

    @classmethod
    def from_p0size(self, p0: Point, size: Size):
        return Rectangle(xmin=p0.x, ymin=p0.y, xmax=(p0.x + size.width), ymax=(p0.y + size.height))

    @classmethod
    def from_centersize(self, center: Point, size: Size):
        xmin = center.x - (size.width/2)
        ymin = center.y - (size.height/2)
        xmax = center.x + (size.width/2)
        ymax = center.y + (size.height/2)
        return Rectangle(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    @classmethod
    def from_labelme_point_list(self, labelme_point_list: list):
        check_list_length(item_list=labelme_point_list, correct_length=2)
        [[xmin, ymin], [xmax, ymax]] = labelme_point_list
        return Rectangle(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

class Polygon:
    def __init__(self, point_list: list):
        check_type_from_list(item_list=point_list, valid_type_list=[Point])
        self.point_list = point_list
        self.rectangle = self._get_rectangle()
        self.rectangle_area = self.rectangle.area

    def _get_rectangle(self) -> Rectangle:
        xmin, ymin = self.point_list[0].x, self.point_list[0].y
        xmax, ymax = self.point_list[0].x, self.point_list[0].y
        for point in self.point_list[1:]:
            if point.x < xmin:
                xmin = point.x
            elif point.x > xmax:
                xmax = point.x
            if point.y < ymin:
                ymin = point.y
            elif point.y > ymax:
                ymax = point.y
        return Rectangle(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def to_labelme_format(self):
        return [[point.x, point.y] for point in self.point_list]

    @classmethod
    def from_labelme_point_list(self, labelme_point_list: list):
        return Polygon([Point(x=item[0], y=item[1]) for item in labelme_point_list])

class Circle:
    def __init__(self, center: Point, radius, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[radius], valid_type_list=number_types)
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Center: ({self.center.x}, {self.center.y}), Radius: {self.radius}"

    def __repr__(self):
        return self.__str__()

class Ellipse:
    def __init__(self, center: Point, size: Size):
        self.center = center
        if size.width == size.height:
            logger.red(f"Invalid Dimensions: size.width == size.height -> {size.width} == {size.height}")
            logger.red(f"You defined a circle. Please use Circle instead.")
            raise Exception
        self.size = size
        self.rectangle = Rectangle(
            xmin=self.center.x-(self.size.width/2),
            ymin=self.center.y-(self.size.height/2),
            xmax=self.center.x+(self.size.width/2),
            ymax=self.center.y+(self.size.height/2)
        )

        self.a = size.width / 2
        self.b = size.height / 2
        self.major = 'x' if self.a > self.b else 'y'
        self.c = (self.a**2 - self.b**2)**0.5 if self.major == 'x' else (self.b**2 - self.a**2)**0.5
        self.e = self.c / self.a if self.major == 'x' else self.c / self.b
        
        self.foci = []
        self.directrix = []
        if self.major == 'x':
            self.foci.append(Point(x=self.center.x+self.c, y=self.center.y))
            self.foci.append(Point(x=self.center.x-self.c, y=self.center.y))
            self.directrix.append(center.x + (self.a / self.e))
            self.directrix.append(center.x - (self.a / self.e)) 
        else:
            self.foci.append(Point(x=self.center.x, y=self.center.y+self.c))
            self.foci.append(Point(x=self.center.x, y=self.center.y-self.c))
            self.directrix.append(center.y + (self.b / self.e))
            self.directrix.append(center.y - (self.b / self.e))

    def __str__(self):
        return f"Center: ({self.center.x}, {self.center.y}), Size: ({self.size.width}, {self.size.height})"

    def __repr__(self):
        return self.__str__()

    def get_equation_str(self, eval_square: bool=False):
        if not eval_square:
            return f'((x-{self.center.x})^2)/({self.a}^2) + ((y-{self.center.y})^2)/({self.b}^2) == 1' 
        else:
            return f'((x-{self.center.x})^2)/{self.a**2} + ((y-{self.center.y})^2)/{self.b**2} == 1'

    def get_area(self):
        return pi * self.a * self.b

    def get_points_given_val(self, given_var: str, given_val):
        solution = []
        if given_var == 'y':
            x_pos = self.center.x + self.a * (1 - (((given_val - self.center.y)**2)/((self.b)**2)))**0.5
            solution.append(Point(x=x_pos, y=given_val))
            x_neg = self.center.x - self.a * (1 - (((given_val - self.center.y)**2)/((self.b)**2)))**0.5
            solution.append(Point(x=x_neg, y=given_val))
        elif given_var == 'x':
            y_pos = self.center.y + self.b * (1 - (((given_val - self.center.x)**2)/((self.a)**2)))**0.5
            solution.append(Point(x=given_val, y=y_pos))
            y_neg = self.center.y - self.b * (1 - (((given_val - self.center.x)**2)/((self.a)**2)))**0.5
            solution.append(Point(x=given_val, y=y_neg))
        else:
            logger.error(f"Invalid given_var: {given_var}")
            logger.error(f"Valid given_var: {['x', 'y']}")
            raise Exception
        return solution

    def get_radius_and_points_given_val(self, given_var: str, given_val):
        points = self.get_points_given_val(given_var=given_var, given_val=given_val)
        point = points[0] # only need one
        radius = ((point.x - self.center.x)**2 + (point.y - self.center.y)**2)**0.5
        return radius, points

    # TODO: Fix this method
    # def get_radius_angle_and_points_given_val(self, given_var: str, given_val, use_deg: bool=True):
    #     radius, points = self.get_radius_and_points_given_val(given_var=given_var, given_val=given_val)
    #     angles = []
    #     if self.major == 'x':
    #         k = (self.b/(radius*self.c))*(self.a**2 + radius**2)**0.5
    #         k = 1.0 if k > 1.0 else 0.0 if k < 0.0 else k
    #         angles.append(asin(k))
    #         angles.append(asin(-k))
    #     elif self.major == 'y':
    #         k = (self.a/(radius*self.c))*(self.b**2 + radius**2)**0.5
    #         k = 1.0 if k > 1.0 else 0.0 if k < 0.0 else k
    #         angles.append(asin(k))
    #         angles.append(asin(-k))
    #     else:
    #         logger.error(f"Invalid given_var: {given_var}")
    #         logger.error(f"Valid given_var: {['x', 'y']}")
    #         raise Exception

    #     if use_deg:
    #         converted = []
    #         for angle in angles:
    #             converted.append(angle * 180 / pi)
    #         angles = converted
    #     return radius, angles, points

class Resize:
    def __init__(self, old_size: Size, new_size: Size):
        self.old_size = old_size
        self.new_size = new_size
        self.w_resize_factor = new_size.width / old_size.width
        self.h_resize_factor = new_size.height / old_size.height

    def on_point(self, point: Point) -> Point:
        return Point(x=point.x*self.w_resize_factor, y=point.y*self.h_resize_factor)

    def on_rectangle(self, rectangle: Rectangle) -> Rectangle:
        p0, p1 = self.on_point(rectangle.p0), self.on_point(rectangle.p1)
        return Rectangle.from_p0p1(p0, p1)

    def on_polygon(self, polygon: Polygon) -> Polygon:
        return Polygon([self.on_point(point) for point in polygon.point_list])

class Interval:
    def __init__(self, min_val, max_val, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[min_val, max_val], valid_type_list=number_types)
        if min_val > max_val:
            logger.error(f"Interval cannot have min_val == {min_val} > max_val == {max_val}")
            raise Exception
        self.min_val = min_val
        self.max_val = max_val

    def __str__(self):
        return f"Interval: [{self.min_val}, {self.max_val}]"

    def __repr__(self):
        return self.__str__()

    def copy(self) -> Interval:
        return Interval(min_val=self.min_val, max_val=self.max_val, check_types=False)

    def to_int(self):
        return Interval(min_val=int(self.min_val), max_val=int(self.max_val), check_types=False)

    def to_float(self):
        return Interval(min_val=float(self.min_val), max_val=float(self.max_val), check_types=False)

    def to_list(self) -> list:
        return [self.min_val, self.max_val]

    def to_tuple(self) -> tuple:
        return (self.min_val, self.max_val)

    def types(self) -> list:
        return [type(self.min_val), type(self.min_val)]

    @classmethod
    def from_list(self, items: list):
        check_list_length(item_list=items, correct_length=2)
        return Interval(min_val=items[0], max_val=items[1])

    def get_length(self):
        return self.max_val - self.min_val

    def center(self) -> float:
        return self.min_val + (0.5 * self.get_length())

    def contains(self, val, bound_type: str='closed') -> bool:
        """
        bound_type
            'closed': Include boundary values
            'open': Exclude boundary values
        """
        check_type(item=val, valid_type_list=number_types)
        check_value(item=bound_type.lower(), valid_value_list=['closed', 'open'])
        if bound_type.lower() == 'closed':
            return self.min_val <= val and val <= self.max_val
        elif bound_type.lower() == 'open':
            return self.min_val < val and val < self.max_val
        else:
            raise Exception

    def contains_interval(self, interval: Interval, bound_type: str='closed') -> bool:
        """
        bound_type
            'closed': Include boundary values
            'open': Exclude boundary values
        """
        if self.contains(val=interval.min_val, bound_type=bound_type) and \
            self.contains(val=interval.max_val, bound_type=bound_type):
            return True
        else:
            return False

    def has_boundary(self, val) -> (bool, str):
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
        if val == self.min_val:
            side = 'left'
            on_boundary = True
        elif val == self.max_val:
            side = 'right'
            on_boundary = True
        return on_boundary, side

    def shift_interval_in_bounds(self, bound: Interval) -> (bool, list, Interval):
        new_interval_min, new_interval_max = self.min_val, self.max_val
        if self.min_val >= bound.min_val and self.max_val <= bound.max_val:
            success = True
            is_left_edge = True if self.min_val == bound.min_val else False
            is_right_edge = True if self.max_val == bound.max_val else False
        elif self.min_val < bound.min_val and self.max_val <= bound.max_val:
            left_deviation = bound.min_val - self.min_val
            new_interval_min = bound.min_val
            new_interval_max += left_deviation
            success = True
            is_left_edge, is_right_edge = True, False
        elif self.min_val >= bound.min_val and self.max_val > bound.max_val:
            right_deviation = self.max_val - bound.max_val
            new_interval_min -= right_deviation
            new_interval_max = self.max_val
            success = True
            is_left_edge, is_right_edge = False, True
        else:
            new_interval_min, new_interval_max = None, None
            success = False
            is_left_edge, is_right_edge = False, False
        
        edge_orientation = [is_left_edge, is_right_edge]
        new_interval = Interval.from_list([new_interval_min, new_interval_max]) \
            if new_interval_min is not None and new_interval_max is not None else None

        if new_interval is not None and not bound.contains_interval(new_interval):
            success = False # One edge was in bounds before shift but then went out of bounds after shift.

        return success, edge_orientation, new_interval

    def split_at(self, val, inclusive_side: str=None) -> (Interval, Interval):
        """
        inclusive_side
            None: val is excluded from both left and right interval
            'left' or 'l': val is included in left interval
            'right' or 'l': val is included in right interval
        """

        def get_interval_pair(val, left_offset: int=0, right_offset: int=0) -> (Interval, Interval):
            left_interval = Interval(self.min_val, val-left_offset) if self.min_val <= val-left_offset else None
            right_interval = Interval(val+right_offset, self.max_val) if val+right_offset <= self.max_val else None
            if left_interval is None or right_interval is None:
                raise Exception
            return left_interval, right_interval

        if inclusive_side is not None:
            check_value(item=inclusive_side.lower(), valid_value_list=['left', 'l', 'right', 'r'])
            # check_type_from_list(item_list=[val, self.min_val, self.max_val], valid_type_list=int_types)
            for val_to_check in [val, self.min_val, self.max_val]:
                if val_to_check not in int_types:
                    inclusive_side = None   # Doing an inclusive split on a non-int interval is the
                                            # same as an exclusive split.
                    logger.warning(f"Attempted an inclusive split on a float interval. Assuming exclusive split.")

        if self.contains(val):
            on_boundary, side = self.has_boundary(val)
            if on_boundary:
                if side == 'right':
                    if inclusive_side is not None: # Inclusive Integer Interval
                        if inclusive_side.lower() in ['left', 'l']:
                            left_interval, right_interval = get_interval_pair(val, right_offset=1)
                        elif inclusive_side.lower() in ['right', 'r']:
                            left_interval, right_interval = self.copy(), None
                        else:
                            raise Exception
                    else: # Exclusive
                        if type(val) in float_types: # Float Interval
                            left_interval, right_interval = get_interval_pair(val)
                        elif type(val) in int_types: # Integer Interval
                            left_interval, right_interval = self.copy(), None
                            left_interval.max_val -= 1
                        else:
                            raise Exception
                elif side == 'left':
                    if inclusive_side is not None: # Inclusive Integer Interval
                        if inclusive_side.lower() in ['left', 'l']:
                            left_interval, right_interval = None, self.copy()
                        elif inclusive_side.lower() in ['right', 'r']:
                            left_interval, right_interval = get_interval_pair(val, left_offset=1)
                        else:
                            raise Exception
                    else: # Exclusive
                        if type(val) in float_types: # Float Interval
                            left_interval, right_interval = get_interval_pair(val)
                        elif type(val) in int_types: # Integer Interval
                            left_interval, right_interval = None, self.copy()
                            right_interval.min_val += 1
                        else:
                            raise Exception
                else:
                    raise Exception
            else: # Not on boundary
                if inclusive_side is not None: # Inclusive Integer Interval
                    if inclusive_side.lower() in ['left', 'l']:
                        left_interval, right_interval = get_interval_pair(val, right_offset=1)
                    elif inclusive_side.lower() in ['right', 'r']:
                        left_interval, right_interval = get_interval_pair(val, left_offset=1)
                    else:
                        raise Exception
                else: # Exclusive
                    if type(val) in float_types: # Float Interval
                        left_interval, right_interval = get_interval_pair(val)
                    elif type(val) in int_types: # Integer Interval
                        left_interval, right_interval = get_interval_pair(val, left_offset=1, right_offset=1)
                    else:
                        raise Exception
        else:
            logger.error(f"val={val} is not in {self.__str__()}")
            raise Exception

        return left_interval, right_interval

    def intersects(self, target_interval: Interval, bound_type: str='closed') -> bool:
        if self.contains(target_interval.min_val, bound_type=bound_type) or \
            self.contains(target_interval.max_val, bound_type=bound_type):
            return True
        else:
            return False

    def intersect(self, target_interval: Interval) -> Interval:
        if not self.intersects(target_interval, bound_type='closed'):
            logger.error(f"Cannot find intersection because target_interval doesn't intersect with host interval.")
            logger.error(f"host interval: {self.__str__()}")
            logger.error(f"target_interval: {target_interval}")
            raise Exception
        min_val = max(self.min_val, target_interval.min_val)
        max_val = min(self.max_val, target_interval.max_val)
        return Interval(min_val=min_val, max_val=max_val, check_types=False)

    def union(self, target_interval: Interval) -> Interval:
        if not self.intersects(target_interval, bound_type='closed'):
            logger.error(f"Cannot find intersection because target_interval doesn't intersect with host interval.")
            logger.error(f"host interval: {self.__str__()}")
            logger.error(f"target_interval: {target_interval}")
            raise Exception
        min_val = min(self.min_val, target_interval.min_val)
        max_val = max(self.max_val, target_interval.max_val)
        return Interval(min_val=min_val, max_val=max_val, check_types=False)

    def shares_exactly_one_bound_with(self, target_interval: Interval) -> bool:
        is_bound0, side0 = self.has_boundary(target_interval.min_val)
        valid0 = is_bound0 and side0 == 'left'
        is_bound1, side1 = self.has_boundary(target_interval.max_val)
        valid1 = is_bound1 and side1 == 'right'
        return (valid0 and not valid1) or (not valid0 and valid1)

    def remove(self, target_interval: Interval) -> Interval:
        is_bound0, side0 = self.has_boundary(target_interval.min_val)
        valid0 = is_bound0 and side0 == 'left'
        is_bound1, side1 = self.has_boundary(target_interval.max_val)
        valid1 = is_bound1 and side1 == 'right'

        if (not valid0 and not valid1) or (valid0 and valid1):
            logger.error(f"Cannot remove target_interval unless exactly one of the boundaries is shared.")
            raise Exception
        elif valid0 and not valid1: # left bound is shared
            return Interval(min_val=target_interval.max_val, max_val=self.max_val, check_types=False)
        elif not valid0 and valid1: # right bound is shared
            return Interval(min_val=self.min_val, max_val=target_interval.min_val, check_types=False)
        else:
            raise Exception