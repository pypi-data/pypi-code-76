from __future__ import annotations
from typing import List
import cv2
import numpy as np
from tqdm import tqdm
from common_utils.file_utils import file_exists
from .streamer import Streamer

class StreamImageIterator:
    def __init__(
        self, src: str, scale_factor: float=1.0,
        show_pbar: bool=False, leave_pbar: bool=False
    ):
        if not isinstance(src, (str, int)):
            raise TypeError(f"Invalid type for src: {type(src).__name__}. Expected str or int.")
        self.src = src
        self.streamer = Streamer(src=src, scale_factor=scale_factor)
        self.stream_type = 'video' if isinstance(src, str) else 'webcam'
        if self.stream_type == 'webcam' and show_pbar:
            raise ValueError(f'Cannot show progress bar for webcam stream.')
        self.pbar = tqdm(total=self.streamer.get_frame_count(), unit='frame(s)', leave=leave_pbar) if show_pbar else None
    
    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> np.ndarray:
        if self.stream_type == 'video':
            continue_condition = self.n < self.streamer.get_frame_count()
        elif self.stream_type == 'webcam':
            continue_condition = self.streamer.is_playing()
        else:
            raise Exception
        if continue_condition:
            img = self.streamer.get_frame()
            self.n += 1
            if self.pbar is not None:
                self.pbar.update()
            return img
        else:
            if self.pbar is not None:
                self.pbar.close()
            raise StopIteration

    def _get_rootname(self, n: int) -> str:
        rootname = str(n)
        while len(rootname) < 6:
            rootname = '0' + rootname
        return rootname

    @property
    def next_img_filename(self) -> str:
        return f'{self._get_rootname(self.n)}.jpg'

    @property
    def current_img_filename(self) -> str:
        return f'{self._get_rootname(self.n - 1)}.jpg'