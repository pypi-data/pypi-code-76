import cv2
import numpy as np
from math import pi, cos, sin, ceil
from typing import List

class SpirographSettings:
    def __init__(self,
        line_color: tuple=(255,0,0), line_thickness: int=1,
        circle_color: tuple=(0,0,255), circle_thickness: int=1
    ):
        self.line_color = line_color
        self.line_thickness = line_thickness
        self.circle_color = circle_color
        self.circle_thickness = circle_thickness

class Spirograph:
    def __init__(
        self, r: float, partitions: int, nodes: List[float],
        settings: SpirographSettings=None
    ):
        self.r = r
        self.partitions = partitions
        self.partition_nodes = [i*2*pi/partitions for i in range(partitions)]
        self.nodes = nodes
        self.settings = settings if settings is not None else SpirographSettings()
    
    def _coord(self, angle: float) -> (int, int):
        x = self.r * cos(angle) + self.r
        y = self.r * sin(angle) + self.r
        return int(x), int(y)
    
    def _draw_circle(self, img: np.ndarray) -> np.ndarray:
        return cv2.circle(
            img=img,
            center=(int(self.r), int(self.r)),
            radius=int(self.r),
            color=self.settings.circle_color,
            thickness=self.settings.circle_thickness
        )
    
    def _draw_line(self, img: np.ndarray, angle0: float, angle1: float) -> np.ndarray:
        pt1, pt2 = self._coord(angle0), self._coord(angle1)
        if pt1 == pt2:
            return img
        else:
            return cv2.line(
                img=img,
                pt1=pt1, pt2=pt2,
                color=self.settings.line_color,
                thickness=self.settings.line_thickness
            )
    
    def _draw_lines(self, img: np.ndarray) -> np.ndarray:
        result = img.copy()
        for angle0 in self.nodes:
            for angle1 in self.partition_nodes:
                result = self._draw_line(
                    img=result,
                    angle0=angle0, angle1=angle1
                )
        return result
    
    def draw(self, img: np.ndarray) -> np.ndarray:
        result = img.copy()
        result = self._draw_circle(img=result)
        result = self._draw_lines(img=result)
        return result
    
    def sample(self) -> np.ndarray:
        img = np.zeros(shape=(ceil(self.r*2), ceil(self.r*2), 3))
        result = self.draw(img)
        return result