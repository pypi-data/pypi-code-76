from __future__ import annotations
import numpy as np
import cv2
from math import floor, ceil
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from imgaug.augmentables.bbs import BoundingBox as ImgAugBBox, BoundingBoxesOnImage as ImgAugBBoxes

from logger import logger
from ..check_utils import check_type_from_list, check_value
from ..utils import get_class_string
from ..file_utils import file_exists
from .common import Point, Interval
from ..constants import number_types
from .point import Point2D, Point2D_List
from .keypoint import Keypoint2D

class BBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        check_type_from_list(item_list=[xmin, ymin, xmax, ymax], valid_type_list=number_types)
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def __str__(self):
        return f"{get_class_string(self)}: (xmin, ymin, xmax, ymax)=({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other: BBox) -> BBox:
        if isinstance(other, BBox):
            xmin = min(self.xmin, other.xmin)
            ymin = min(self.ymin, other.ymin)
            xmax = max(self.xmax, other.xmax)
            ymax = max(self.ymax, other.ymax)
            return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax).to_float()
        elif isinstance(other, (int, float)):
            return BBox(xmin=self.xmin+other, ymin=self.ymin+other, xmax=self.xmax+other, ymax=self.ymax+other)
        elif isinstance(other, Point2D):
            return BBox(xmin=self.xmin+other.x, ymin=self.ymin+other.y, xmax=self.xmax+other.x, ymax=self.ymax+other.y)
        elif isinstance(other, Keypoint2D):
            return BBox(xmin=self.xmin+other.point.x, ymin=self.ymin+other.point.y, xmax=self.xmax+other.point.x, ymax=self.ymax+other.point.y)
        else:
            logger.error(f'Cannot add {type(other)} to BBox')
            raise TypeError

    def __sub__(self, other) -> BBox:
        if isinstance(other, BBox):
            raise NotImplementedError
        elif isinstance(other, (int, float)):
            return BBox(xmin=self.xmin-other, ymin=self.ymin-other, xmax=self.xmax-other, ymax=self.ymax-other)
        elif isinstance(other, Point2D):
            return BBox(xmin=self.xmin-other.x, ymin=self.ymin-other.y, xmax=self.xmax-other.x, ymax=self.ymax-other.y)
        elif isinstance(other, Keypoint2D):
            return BBox(xmin=self.xmin-other.point.x, ymin=self.ymin-other.point.y, xmax=self.xmax-other.point.x, ymax=self.ymax-other.point.y)
        else:
            logger.error(f'Cannot subtract {type(other)} from BBox')
            raise TypeError

    def __mul__(self, other) -> BBox:
        if isinstance(other, (int, float)):
            return BBox(xmin=self.xmin*other, ymin=self.ymin*other, xmax=self.xmax*other, ymax=self.ymax*other)
        else:
            logger.error(f'Cannot multiply {type(other)} with BBox')
            raise TypeError


    def __truediv__(self, other) -> BBox:
        if isinstance(other, (int, float)):
            return BBox(xmin=self.xmin/other, ymin=self.ymin/other, xmax=self.xmax/other, ymax=self.ymax/other)
        else:
            logger.error(f'Cannot divide {type(other)} from BBox')
            raise TypeError

    def __eq__(self, other: BBox) -> bool:
        if isinstance(other, BBox):
            return self.xmin == other.xmin and self.ymin == other.ymin and self.xmax == other.xmax and self.ymax == other.ymax
        else:
            return NotImplemented

    @property
    def pmin(self) -> Point2D:
        return Point2D(x=self.xmin, y=self.ymin)
    
    @property
    def pmax(self) -> Point2D:
        return Point2D(x=self.xmax, y=self.ymax)

    @classmethod
    def buffer(self, bbox: BBox) -> BBox:
        return bbox

    def copy(self) -> BBox:
        return BBox(
            xmin=self.xmin,
            ymin=self.ymin,
            xmax=self.xmax,
            ymax=self.ymax
        )

    def to_int(self) -> BBox:
        return BBox(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax)
        )
    
    def to_rounded_int(self, special: bool=False) -> BBox:
        """Rounds BBox object to have integer coordinates.

        Keyword Arguments:
            special {bool} -- [Round xmin and ymin down using floor, and round xmax and ymax usin ceil.] (default: {False})

        Returns:
            BBox -- [description]
        """
        if not special:
            return BBox(
                xmin=round(self.xmin),
                ymin=round(self.ymin),
                xmax=round(self.xmax),
                ymax=round(self.ymax)
            )
        else:
            return BBox(
                xmin=floor(self.xmin),
                ymin=floor(self.ymin),
                xmax=ceil(self.xmax),
                ymax=ceil(self.ymax)
            )

    def to_float(self) -> BBox:
        return BBox(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax)
        )

    def to_list(self, output_format: str='pminpmax') -> list:
        """
        output_format options:
            'pminpmax': [xmin, ymin, xmax, ymax]
            'pminsize': [xmin, ymin, width, height]
        """
        check_value(output_format, valid_value_list=['pminpmax', 'pminsize'])
        if output_format == 'pminpmax':
            return [self.xmin, self.ymin, self.xmax, self.ymax]
        elif output_format == 'pminsize':
            bbox_h, bbox_w = self.shape()
            return [self.xmin, self.ymin, bbox_w, bbox_h]
        else:
            raise Exception

    @classmethod
    def from_list(self, bbox: list, input_format: str='pminpmax') -> BBox:
        """
        input_format options:
            'pminpmax': [xmin, ymin, xmax, ymax]
            'pminsize': [xmin, ymin, width, height]
        """
        check_value(input_format, valid_value_list=['pminpmax', 'pminsize'])
        if input_format == 'pminpmax':
            xmin, ymin, xmax, ymax = bbox
            return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
        elif input_format == 'pminsize':
            xmin, ymin, bbox_w, bbox_h = bbox
            xmax, ymax = xmin + bbox_w, ymin + bbox_h
            return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
        else:
            raise Exception

    def to_shapely(self) -> ShapelyPolygon:
        p0 = [self.xmin, self.ymin]
        p1 = [self.xmax, self.ymin]
        p2 = [self.xmax, self.ymax]
        p3 = [self.xmin, self.ymax]
        return ShapelyPolygon([p0, p1, p2, p3])

    @classmethod
    def from_shapely(self, shapely_polygon: ShapelyPolygon) -> BBox:
        vals_tuple = shapely_polygon.exterior.coords.xy
        numpy_array = np.array(vals_tuple).T[:-1]
        if numpy_array.shape != (4, 2):
            logger.error(f"Expected shapely object of size (4, 2). Got {numpy_array.shape}")
            raise Exception
        xmin, ymin = numpy_array.min(axis=0)
        xmax, ymax = numpy_array.max(axis=0)
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def to_imgaug(self) -> ImgAugBBox:
        return ImgAugBBox(x1=self.xmin, y1=self.ymin, x2=self.xmax, y2=self.ymax)

    @classmethod
    def from_imgaug(cls, imgaug_bbox: ImgAugBBox) -> BBox:
        return BBox(
            xmin=imgaug_bbox.x1,
            ymin=imgaug_bbox.y1,
            xmax=imgaug_bbox.x2,
            ymax=imgaug_bbox.y2
        )

    @classmethod
    def from_p0p1(cls, p0p1: np.ndarray) -> BBox:
        """
        Parses from format np.ndarray([[x0, y0], [x1, y1]]), where
        it is not known which values are min and max.
        """
        if type(p0p1) is list:
            arr = np.array(p0p1)
        elif type(p0p1) is np.ndarray:
            arr = p0p1.copy()
        else:
            raise TypeError
        if arr.shape != (2,2):
            logger.error(f'arr.shape == {arr.shape} != (2,2)')
            raise Exception
        xmin, ymin = arr.min(axis=0)
        xmax, ymax = arr.max(axis=0)
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def to_point2d_list(self) -> Point2D_List:
        arr = np.array(self.to_list(output_format='pminpmax'))
        return Point2D_List.from_numpy(arr.reshape(2,2))

    @classmethod
    def from_point2d_list(cls, point2d_list: Point2D_List) -> BBox:
        return BBox.from_p0p1(p0p1=point2d_list.to_numpy(demarcation=True))

    @property
    def width(self) -> float:
        return float(self.xmax - self.xmin)
    
    @property
    def height(self) -> float:
        return float(self.ymax - self.ymin)

    def area(self) -> float:
        return float(self.width * self.height)

    def shape(self) -> list:
        """
        return [height, width]
        """
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return [height, width]

    def center(self) -> list:
        x_center = 0.5 * (self.xmin + self.xmax)
        y_center = 0.5 * (self.ymin + self.ymax)
        return [x_center, y_center]

    def aspect_ratio(self) -> float:
        """
        aspect ratio is height:width
        """
        height, width = self.shape()
        return height / width

    def contains(self, obj) -> bool:
        return self.to_shapely().contains(obj.to_shapely())

    def within(self, obj) -> bool:
        return self.to_shapely().within(obj.to_shapely())

    def resize(self, orig_frame_shape: list, new_frame_shape: list) -> BBox:
        h, w = orig_frame_shape[:2]
        target_h, target_w = new_frame_shape[:2]
        w_scale, h_scale = target_w / w, target_h / h
        return BBox(xmin=self.xmin*w_scale, ymin=self.ymin*h_scale, xmax=self.xmax*w_scale, ymax=self.ymax*h_scale)

    def rescale(self, target_shape: list, fixed_point: Point) -> BBox:
        if fixed_point.x < self.xmin or fixed_point.x > self.xmax or \
            fixed_point.y < self.ymin or fixed_point.y > self.ymax:
            logger.error(f"fixed point {fixed_point} not inside bbox {self}")
            raise Exception
        left_dx, right_dx = fixed_point.x - self.xmin, self.xmax - fixed_point.x
        left_dy, right_dy = fixed_point.y - self.ymin, self.ymax - fixed_point.y
        bbox_h, bbox_w = self.shape()
        target_h, target_w = target_shape[:2]
        h_scale_factor, w_scale_factor = target_h / bbox_h, target_w / bbox_w
        new_left_dx, new_right_dx = left_dx * w_scale_factor, right_dx * w_scale_factor
        new_left_dy, new_right_dy = left_dy * h_scale_factor, right_dy * h_scale_factor
        new_xmin, new_xmax = fixed_point.x - new_left_dx, fixed_point.x + new_right_dx
        new_ymin, new_ymax = fixed_point.y - new_left_dy, fixed_point.y + new_right_dy
        new_bbox = BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
        return new_bbox

    def is_inside_of(self, bbox: self) -> bool:
        x_is_inside = True if bbox.xmin <= self.xmin and self.xmax <= bbox.xmax else False
        y_is_inside = True if bbox.ymin <= self.ymin and self.ymax <= bbox.ymax else False
        return x_is_inside and y_is_inside

    def encloses(self, bbox: self) -> bool:
        x_encloses = True if self.xmin <= bbox.xmin and bbox.xmax <= self.xmax else False
        y_encloses = True if self.ymin <= bbox.ymin and bbox.ymax <= self.ymax else False
        return x_encloses and y_encloses

    def overlaps_with(self, bbox: self) -> bool:
        x_overlaps = True if (bbox.xmin < self.xmin and self.xmin < bbox.xmax) \
            or (bbox.xmin < self.xmax and self.xmax < bbox.xmax) else False
        y_overlaps = True if (bbox.ymin < self.ymin and self.ymin < bbox.ymax) \
            or (bbox.ymin < self.ymax and self.ymax < bbox.ymax) else False
        return x_overlaps or y_overlaps

    def is_adjacent_with(self, bbox: self) -> bool:
        is_x_adjacent = True if bbox.xmax == self.xmin or self.xmax == bbox.xmin else False
        is_y_adjacent = True if bbox.ymax == self.ymin or self.ymax == bbox.ymin else False
        return is_x_adjacent and is_y_adjacent

    def center_is_inside_of(self, bbox: self) -> bool:
        cx, cy = self.center()
        x_is_inside = True if bbox.xmin <= cx and cx <= bbox.xmax else False
        y_is_inside = True if bbox.ymin <= cy and cy <= bbox.ymax else False
        return x_is_inside and y_is_inside

    def check_bbox_in_frame(self, frame_shape: list):
        frame_h, frame_w = frame_shape[:2]
        frame_box = BBox.from_list([0, 0, frame_w, frame_h])
        if not self.is_inside_of(frame_box):
            logger.error(f"bbox is not inside of frame_box")
            logger.error(f"bbox: {self.__str__()}")
            logger.error(f"frame_box: {frame_box}")
            raise Exception

    def check_bbox_aspect_ratio(self, target_aspect_ratio: float):
        if abs(self.aspect_ratio() - target_aspect_ratio) > 0.01:
            logger.error(f"Not creating the correct aspect ratio")
            logger.error(f"Target: {target_aspect_ratio}, actual: {self.aspect_ratio()}")
            raise Exception

    def pad(self, target_aspect_ratio: list, direction: str) -> BBox:
        """
        target_aspect_ratio corresponds to target_height:target_width
        """
        check_value(item=direction, valid_value_list=['x', 'y'])
        bbox_h, bbox_w = self.shape()
        bbox_cx, bbox_cy = self.center()

        if direction == 'x':
            target_bbox_h = bbox_h
            new_bbox_ymin, new_bbox_ymax = self.ymin, self.ymax
            target_bbox_w = bbox_h / target_aspect_ratio
            new_bbox_xmin, new_bbox_xmax = \
                bbox_cx - (0.5 * target_bbox_w), bbox_cx + (0.5 * target_bbox_w)
        elif direction == 'y':
            target_bbox_w = bbox_w
            new_bbox_xmin, new_bbox_xmax = self.xmin, self.xmax
            target_bbox_h = bbox_w * target_aspect_ratio
            new_bbox_ymin, new_bbox_ymax = \
                bbox_cy - (0.5 * target_bbox_h), bbox_cy + (0.5 * target_bbox_h)
        else:
            raise Exception

        return BBox.from_list([new_bbox_xmin, new_bbox_ymin, new_bbox_xmax, new_bbox_ymax])

    def is_adjacent_to_frame_bounds(self, frame_shape: list) -> (bool, bool, bool, bool):
        """
        returns: left_adjacent, top_adjacent, right_adjacent, bottom_adjacent
        """
        frame_h, frame_w = frame_shape[:2]
        left_adjacent = True if self.xmin == 0 else False
        top_adjacent = True if self.ymin == 0 else False
        right_adjacent = True if self.xmax == frame_w - 1 else False
        bottom_adjacent = True if self.ymax == frame_h - 1 else False
        return left_adjacent, top_adjacent, right_adjacent, bottom_adjacent

    def clip_at_bounds(self, frame_shape: list) -> BBox:
        frame_h, frame_w = frame_shape[:2]
        xmin = 0 if self.xmin < 0 else frame_w - 1 if self.xmin >= frame_w else self.xmin
        ymin = 0 if self.ymin < 0 else frame_h - 1 if self.ymin >= frame_h else self.ymin
        xmax = 0 if self.xmax < 0 else frame_w - 1 if self.xmax >= frame_w else self.xmax
        ymax = 0 if self.ymax < 0 else frame_h - 1 if self.ymax >= frame_h else self.ymax
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def scale_about_center(self, scale_factor: float, frame_shape: list) -> BBox:
        frame_h, frame_w = frame_shape[:2]
        bbox = self.copy()
        bbox_h, bbox_w = bbox.shape()
        dx = bbox_w * (scale_factor - 1.0) / 2
        dy = bbox_h * (scale_factor - 1.0) / 2            
        bbox.xmin -= dx
        bbox.ymin -= dy
        bbox.xmax += dx
        bbox.ymax += dy
        bbox = bbox.clip_at_bounds(frame_shape=[frame_h, frame_w])
        return bbox

    def crop_from(self, img: np.ndarray) -> np.ndarray:
        img_h, img_w = img.shape[:2]
        int_bbox = self.to_int()
        if len(img.shape) == 3:
            return img[int_bbox.ymin:int_bbox.ymax, int_bbox.xmin:int_bbox.xmax, :]
        elif len(img.shape) == 2:
            return img[int_bbox.ymin:int_bbox.ymax, int_bbox.xmin:int_bbox.xmax]
        else:
            logger.error(f'Expected len(img.shape) to be either 2 or 3. Encountered len(img.shape) == {len(img.shape)}')
            raise Exception
    
    def crop_and_paste(self, src_img: np.ndarray, dst_img: np.ndarray, dst_bbox: BBox=None) -> np.ndarray:
        self.check_bbox_in_frame(src_img.shape)
        if dst_bbox is not None:
            dst_bbox.check_bbox_in_frame(dst_img.shape)
        else:
            self.check_bbox_in_frame(dst_img.shape)
        result = dst_img.copy()
        cropped_img = self.crop_from(src_img)
        if dst_bbox is not None:
            if dst_bbox.shape != cropped_img.shape[:2]:
                cropped_img = cv2.resize(src=cropped_img, dsize=(dst_bbox.width, dst_bbox.height))
            result[int(dst_bbox.ymin):int(dst_bbox.ymax), int(dst_bbox.xmin):int(dst_bbox.xmax), :] = cropped_img
        else:
            result[int(self.ymin):int(self.ymax), int(self.xmin):int(self.xmax), :] = cropped_img
        return result

    def crop_from_and_save_to(self, img: np.ndarray, save_path: str, overwrite: bool=False):
        cropped_region = self.crop_from(img=img)
        if file_exists(save_path) and not overwrite:
            logger.error(f'File already exists at {save_path}')
            logger.error(f'Hint: Use overwrite=True')
            raise Exception
        else:
            cv2.imwrite(filename=save_path, img=cropped_region)

    def is_valid(self) -> bool:
        return self.xmin < self.xmax and self.ymin < self.ymax

    def intersect_with(self, other: BBox, check_valid: bool=True) -> BBox:
        if isinstance(other, BBox):
            xmin = max(self.xmin, other.xmin)
            ymin = max(self.ymin, other.ymin)
            xmax = min(self.xmax, other.xmax)
            ymax = min(self.ymax, other.ymax)
            result = BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax).to_float()
            if check_valid:
                if not result.is_valid():
                    logger.error(f'Result of intersection is invalid.')
                    logger.error(f'result: {result}')
                    logger.error(f'The two bounding boxes are likely not overlapping.')
                    raise Exception
            return result
        else:
            logger.error(f'Cannot intersect BBox with {type(other)}')
            raise Exception
    
    def iou(self, other: BBox) -> float:
        if isinstance(other, BBox):
            intersection = self.intersect_with(other, check_valid=False)
            if intersection.is_valid():
                intersection_area = intersection.area()
                union_area = self.area() + (other.area() - intersection_area)
                return intersection_area / union_area
            else:
                return 0.0
        else:
            logger.error(f'Cannot calculate iou of BBox with {type(other)}')
            raise Exception

class ConstantAR_BBox(BBox):
    def __init__(self, xmin, ymin, xmax, ymax):
        super().__init__(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
        self.requires_zero_pad = False
        self.left_offset = None
        self.right_offset = None
        self.up_offset = None
        self.down_offset = None

    def from_BBox(self, bbox: BBox) -> ConstantAR_BBox:
        return ConstantAR_BBox(xmin=bbox.xmin, ymin=bbox.ymin, xmax=bbox.xmax, ymax=bbox.ymax)

    @classmethod
    def buffer(self, bbox: ConstantAR_BBox) -> ConstantAR_BBox:
        return bbox

    def copy(self) -> ConstantAR_BBox:
        return ConstantAR_BBox(
            xmin=self.xmin,
            ymin=self.ymin,
            xmax=self.xmax,
            ymax=self.ymax
        )

    def to_int(self) -> ConstantAR_BBox:
        return ConstantAR_BBox(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax)
        )

    def to_float(self) -> ConstantAR_BBox:
        return ConstantAR_BBox(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax)
        )

    @classmethod
    def from_list(self, bbox: list) -> ConstantAR_BBox:
        xmin, ymin, xmax, ymax = bbox
        return ConstantAR_BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def rescale(self, target_shape: list, fixed_point: Point) -> ConstantAR_BBox:
        return self.from_BBox(super().rescale(target_shape=target_shape, fixed_point=fixed_point))

    def pad(self, target_aspect_ratio: list, direction: str) -> ConstantAR_BBox:
        return self.from_BBox(super().pad(target_aspect_ratio=target_aspect_ratio, direction=direction))

    def is_in_bounds(self, frame_shape: list) -> bool:
        frame_h, frame_w = frame_shape[:2]
        xmin_in_bounds = True if 0 <= self.xmin <= frame_w - 1 else False
        xmax_in_bounds = True if 0 <= self.xmax <= frame_w - 1 else False
        ymin_in_bounds = True if 0 <= self.ymin <= frame_h - 1 else False
        ymax_in_bounds = True if 0 <= self.ymax <= frame_h - 1 else False
        return xmin_in_bounds and xmax_in_bounds and ymin_in_bounds and ymax_in_bounds

    def adjust_to_frame_bounds(self, frame_shape: list) -> ConstantAR_BBox:
        xmin, ymin, xmax, ymax = self.to_list()
        frame_h, frame_w = frame_shape[:2]
        xmin = 0 if xmin < 0 else frame_w - 1 if xmin >= frame_w else xmin
        ymin = 0 if ymin < 0 else frame_h - 1 if ymin >= frame_h else ymin
        xmax = 0 if xmax < 0 else frame_w - 1 if xmax >= frame_w else xmax
        ymax = 0 if ymax < 0 else frame_h - 1 if ymax >= frame_h else ymax
        result = ConstantAR_BBox.from_list([xmin, ymin, xmax, ymax])
        result.check_bbox_in_frame(frame_shape=frame_shape)
        return result

    def shift_bbox_in_bounds(self, frame_shape: list) -> (list, list, list):
        frame_h, frame_w = frame_shape[:2]
        x_interval = Interval.from_list([self.xmin, self.xmax])
        y_interval = Interval.from_list([self.ymin, self.ymax])
        x_bound = Interval.from_list([0, frame_w])
        y_bound = Interval.from_list([0, frame_h])
        x_is_in_bounds, [is_left_edge, is_right_edge], new_x_interval = \
            x_interval.shift_interval_in_bounds(bound=x_bound)
        y_is_in_bounds, [is_top_edge, is_bottom_edge], new_y_interval = \
            y_interval.shift_interval_in_bounds(bound=y_bound)
        [new_xmin, new_xmax] = new_x_interval.to_list() \
            if new_x_interval is not None else [None, None]
        [new_ymin, new_ymax] = new_y_interval.to_list() \
            if new_y_interval is not None else [None, None]
        bounds = [x_is_in_bounds, y_is_in_bounds]
        edge_orientation = [is_left_edge, is_right_edge, is_top_edge, is_bottom_edge]
        new_rect = [new_xmin, new_ymin, new_xmax, new_ymax]
        return bounds, edge_orientation, new_rect

    def rescale_bbox(self, target_aspect_ratio: list, pad_direction: str, mode: str='c') -> ConstantAR_BBox:
        mode = mode.lower()
        check_value(item=pad_direction.lower(), valid_value_list=['w', 'width', 'h', 'height'])
        check_value(item=mode, valid_value_list=['c', 'ct', 'cb', 'cr', 'cl', 'tr', 'tl', 'br', 'bl'])
        
        bbox_h, bbox_w = self.shape()
        if pad_direction.lower() in ['w', 'width']:
            target_w = bbox_w
            target_h = bbox_w * target_aspect_ratio
        elif pad_direction.lower() in ['h', 'height']:
            target_h = bbox_h
            target_w = bbox_h / target_aspect_ratio
        else:
            raise Exception

        target_shape = [target_h, target_w]

        [cx, cy] = self.center()
        top, bottom = self.ymin, self.ymax
        left, right = self.xmin, self.xmax

        if mode == 'c':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([cx, cy]))
        elif mode == 'ct':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([cx, top]))
        elif mode == 'cb':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([cx, bottom]))
        elif mode == 'cr':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([right, cy]))
        elif mode == 'cl':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([left, cy]))
        elif mode == 'tr':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([right, top]))
        elif mode == 'tl':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([left, top]))
        elif mode == 'br':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([right, bottom]))
        elif mode == 'bl':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([left, bottom]))
        else:
            raise Exception
        result.check_bbox_aspect_ratio(target_aspect_ratio=target_aspect_ratio)
        return result

    def rescale_shift_bbox(self, frame_shape: list, target_aspect_ratio: float, pad_direction: str, mode: str='c') -> (list, list, list):
        result = self.rescale_bbox(target_aspect_ratio=target_aspect_ratio, pad_direction=pad_direction, mode=mode)
        bounds, edge_orientation, new_rect = result.shift_bbox_in_bounds(frame_shape=frame_shape)
        return bounds, edge_orientation, new_rect

    def rescale_shift_until_valid(self, frame_shape: list, target_aspect_ratio: float, max_retry_count: int=5) -> ConstantAR_BBox:
        result = self
        mode = 'c'
        pad_direction = 'height'
        frame_h, frame_w = frame_shape[:2]
        retry_count = -1
        success = False

        backup = self.copy()

        while retry_count < max_retry_count:
            retry_count += 1
            bounds, edge_orientation, new_rect = result.rescale_shift_bbox(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio, pad_direction=pad_direction, mode=mode)
            [x_is_in_bounds, y_is_in_bounds] = bounds
            [is_left_edge, is_right_edge, is_top_edge, is_bottom_edge] = edge_orientation
            [new_xmin, new_ymin, new_xmax, new_ymax] = new_rect
            if x_is_in_bounds and y_is_in_bounds:
                success = True
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
                break
            elif x_is_in_bounds and not y_is_in_bounds:
                new_ymin, new_ymax = 0, frame_h
                pad_direction = 'width'
                if is_left_edge and not is_right_edge:
                    mode = 'cl'
                elif is_right_edge and not is_left_edge:
                    mode = 'cr'
                else:
                    mode = 'c'
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
            elif not x_is_in_bounds and y_is_in_bounds:
                new_xmin, new_xmax = 0, frame_w
                pad_direction = 'height'
                if is_top_edge and not is_bottom_edge:
                    mode = 'ct'
                elif is_bottom_edge and not is_top_edge:
                    mode = 'cb'
                else:
                    mode = 'c'
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
            elif not x_is_in_bounds and not y_is_in_bounds:
                new_ymin, new_ymax = 0, frame_h
                new_xmin, new_xmax = 0, frame_w
                pad_direction = 'height'
                mode = 'c'
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
            else:
                raise Exception

        if not success:
            logger.error(f"Couldn't obtain target aspect ratio within {max_retry_count} retries.")
            raise Exception

        result.check_bbox_aspect_ratio(target_aspect_ratio=target_aspect_ratio)
        return result

    def rescale_to_ar(self, target_aspect_ratio: float, hold_direction: str, hold_mode: str='center'):
        hold_direction = hold_direction.lower()
        check_value(item=hold_direction, valid_value_list=['x', 'y'])
        hold_mode = hold_mode.lower()
        check_value(item=hold_mode, valid_value_list=['center', 'min', 'max'])

        result = self.copy()
        if hold_direction == 'x':
            new_xmin, new_xmax = result.xmin, result.xmax
            new_width = new_xmax - new_xmin
            new_height = new_width * target_aspect_ratio
            if hold_mode == 'min':
                new_ymin = result.ymin
                new_ymax = new_ymin + new_height
            elif hold_mode == 'max':
                new_ymax = result.ymax
                new_ymin = new_ymax - new_height
            elif hold_mode == 'center':
                cy = 0.5 * (result.ymin + result.ymax)
                new_ymin = cy - (0.5 * new_height)
                new_ymax = cy + (0.5 * new_height)
            else:
                raise Exception
        elif hold_direction == 'y':
            new_ymin, new_ymax = result.ymin, result.ymax
            new_height = new_ymax - new_ymin
            new_width = new_height / target_aspect_ratio
            if hold_mode == 'min':
                new_xmin = result.xmin
                new_xmax = new_xmin + new_width
            elif hold_mode == 'max':
                new_xmax = result.xmax
                new_xmin = new_xmax - new_width
            elif hold_mode == 'center':
                cx = 0.5 * (result.xmin + result.xmax)
                new_xmin = cx - (0.5 * new_width)
                new_xmax = cx + (0.5 * new_width)
            else:
                raise Exception
        else:
            raise Exception
        return ConstantAR_BBox(xmin=new_xmin, ymin=new_ymin, xmax=new_xmax, ymax=new_ymax)

    def upscale_to_ar(self, target_aspect_ratio: float, hold_mode: str='center') -> ConstantAR_BBox:
        hold_mode = hold_mode.lower()
        check_value(item=hold_mode, valid_value_list=['center', 'min', 'max'])
        result = self.copy()

        aspect_ratio = result.aspect_ratio()
        if aspect_ratio > target_aspect_ratio: # too tall; expand width, hold y
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='y', hold_mode=hold_mode)
        else: # too wide; expand height, hold x
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='y', hold_mode=hold_mode)
        return result

    def downscale_to_ar(self, target_aspect_ratio: float, hold_mode: str='center') -> ConstantAR_BBox:
        hold_mode = hold_mode.lower()
        check_value(item=hold_mode, valid_value_list=['center', 'min', 'max'])
        result = self.copy()

        aspect_ratio = result.aspect_ratio()
        if aspect_ratio > target_aspect_ratio: # too tall; shrink height, hold x
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='x', hold_mode=hold_mode)
        else: # too wide; shrink width, hold y
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='y', hold_mode=hold_mode)
        return result

    def try_upscale_to_ar(self, frame_shape: list, target_aspect_ratio: float, hold_mode: str) -> ConstantAR_BBox:
        """
        Attempt upscale.
        Return None if bbox goes out of bounds.
        """
        result = self.copy()
        result = result.upscale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_mode=hold_mode)
        if result.is_in_bounds(frame_shape=frame_shape):
            return result
        else:
            return None

    def try_downscale_to_ar(self, frame_shape: list, target_aspect_ratio: float, hold_mode: str) -> ConstantAR_BBox:
        """
        Attempt downscale.
        Return None if bbox goes out of bounds.
        """
        result = self.copy()
        result = result.downscale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_mode=hold_mode)
        result = result.to_int()
        if result.is_in_bounds(frame_shape=frame_shape):
            return result
        else:
            return None

    def crop_scale(self, frame_shape: list, target_aspect_ratio: float) -> ConstantAR_BBox:
        """
        1. First try upscale.
        2. Try downscale if upscale doesn't work.
        3. Preserve frame border adjacent sides of the bbox.
        """
        result = self.copy()
        result = result.adjust_to_frame_bounds(frame_shape=frame_shape)
        left_adj, top_adj, right_adj, bottom_adj = result.is_adjacent_to_frame_bounds(frame_shape)

        not_adj = not left_adj and not top_adj and not right_adj and not bottom_adj
        l_adj = left_adj and not top_adj and not right_adj and not bottom_adj
        t_adj = not left_adj and top_adj and not right_adj and not bottom_adj
        r_adj = not left_adj and not top_adj and right_adj and not bottom_adj
        b_adj = not left_adj and not top_adj and not right_adj and bottom_adj

        lt_adj = left_adj and top_adj
        rt_adj = right_adj and top_adj
        lb_adj = left_adj and bottom_adj
        rb_adj = right_adj and bottom_adj

        approach = 'upscale'

        if not_adj:
            hold_mode = 'center'
        elif l_adj or t_adj or lt_adj or rt_adj or lb_adj:
            hold_mode = 'min'
        elif rb_adj:
            hold_mode = 'max'
        else:
            hold_mode = 'center'

        while True:
            new_result = result.copy()
            if approach == 'upscale':
                new_result = new_result.try_upscale_to_ar(
                    frame_shape=frame_shape,
                    target_aspect_ratio=target_aspect_ratio,
                    hold_mode=hold_mode
                )
                if new_result is not None:
                    result = new_result
                    break
                else:
                    approach = 'downscale'
            elif approach == 'downscale':
                new_result = new_result.try_downscale_to_ar(
                    frame_shape=frame_shape,
                    target_aspect_ratio=target_aspect_ratio,
                    hold_mode=hold_mode
                )
                if new_result is not None:
                    result = new_result
                    break
                else:
                    logger.error(f"Couldn't resolve bbox.")
                    raise Exception
        return result

    def square_pad(self, frame_shape: list, side_mode: str='max') -> ConstantAR_BBox:
        check_value(side_mode, valid_value_list=['max', 'min'])
        frame_h, frame_w = frame_shape[:2]
        
        result = self.copy()
        result = result.adjust_to_frame_bounds(frame_shape=frame_shape)

        if side_mode == 'max':
            target_side_length = max(self.shape())
        elif side_mode == 'min':
            target_side_length = min(self.shape())
        else:
            raise Exception
        target_side_length = frame_h if target_side_length > frame_h else target_side_length
        target_side_length = frame_w if target_side_length > frame_w else target_side_length

        [cx, cy] = result.center()
        new_xmin, new_xmax = cx - (0.5 * target_side_length), cx + (0.5 * target_side_length)
        new_ymin, new_ymax = cy - (0.5 * target_side_length), cy + (0.5 * target_side_length)
        new_result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
        if new_result.is_in_bounds(frame_shape=frame_shape):
            return new_result
        else:
            _, _, new_rect = new_result.shift_bbox_in_bounds(frame_shape=frame_shape)
            new_result = ConstantAR_BBox.from_list(new_rect)
            if new_result.is_in_bounds(frame_shape=frame_shape):
                return new_result
            else:
                bbox_h, bbox_w = new_result.shape()
                old_xmin, old_ymin, old_xmax, old_ymax = new_result.to_list()
                left_offset = old_xmin - 0 if old_xmin - 0 > 0 else 0
                right_offset = old_xmax - (frame_w - 1) if old_xmax - (frame_w - 1) > 0 else 0
                up_offset = old_ymin - 0 if old_ymin - 0 > 0 else 0
                down_offset = old_ymax - (frame_h - 1) if old_ymax - (frame_h - 1) > 0 else 0
                xmin, xmax = old_xmin + left_offset, old_xmax + left_offset
                ymin, ymax = old_ymin + up_offset, old_ymax + up_offset
                new_result = ConstantAR_BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
                new_result.requires_zero_pad = True
                new_result.left_offset, new_result.right_offset = left_offset, right_offset
                new_result.up_offset, new_result.down_offset = up_offset, down_offset
                return new_result
                # if side_mode == 'max':
                #     return self.square_pad(frame_shape=frame_shape, side_mode='min')
                # else:
                #     logger.error(f"Couldn't resolve bbox.")
                #     raise Exception

    def adjust_to_target_shape(
        self, frame_shape: list, target_shape: list, method: str='conservative_pad'
    ) -> ConstantAR_BBox:
        check_value(item=method, valid_value_list=['pad', 'conservative_pad'])
        result = self
        target_h, target_w = target_shape[:2]
        target_aspect_ratio = target_h / target_w
        if method == 'pad':
            result = result.rescale_shift_until_valid(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio, max_retry_count=5)
            result.check_bbox_in_frame(frame_shape=frame_shape)
        elif method == 'conservative_pad':
            result = result.crop_scale(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio)
        else:
            raise Exception
        return result