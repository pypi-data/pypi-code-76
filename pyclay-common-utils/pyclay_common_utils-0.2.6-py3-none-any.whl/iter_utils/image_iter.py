from __future__ import annotations
from typing import List
import cv2
import numpy as np
from tqdm import tqdm
from ..file_utils import file_exists, dir_exists
from ..path_utils import get_valid_image_paths, get_filename

class ImageIterator:
    def __init__(
        self, img_paths: List[str], check_paths: bool=True,
        show_pbar: bool=False, leave_pbar: bool=False,
        pbar_desc_mode: str='filename'
    ):
        if isinstance(img_paths, list):
            if not all([isinstance(img_path, str) for img_path in img_paths]):
                raise TypeError(f"img_paths must be a list of strings.")
        else:
            raise TypeError(f"img_paths must be a list of strings.")
        if check_paths:
            for img_path in img_paths:
                if not file_exists(img_path):
                    raise FileNotFoundError(f"Couldn't find image at {img_path}")

        self.img_paths = img_paths

        valid_pbar_desc_modes = [
            'filename',
            'index'
        ]
        if show_pbar and pbar_desc_mode not in valid_pbar_desc_modes:
            raise ValueError(
                f"""
                Invalid value for pbar_desc_mode: {pbar_desc_mode}
                Valid values: {valid_pbar_desc_modes}
                """
            )
        self.pbar_desc_mode = pbar_desc_mode
        self.pbar = tqdm(total=len(self.img_paths), unit='image(s)', leave=leave_pbar) if show_pbar else None
    
    @property
    def next_img_path(self) -> str:
        return self.img_paths[self.n]

    @property
    def next_img_filename(self) -> str:
        return get_filename(self.next_img_path)

    @property
    def current_img_path(self) -> str:
        return self.img_paths[self.n-1]
    
    @property
    def current_img_filename(self) -> str:
        return get_filename(self.current_img_path)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> np.ndarray:
        if self.n < len(self.img_paths):
            img = cv2.imread(self.next_img_path)
            self.n += 1
            if self.pbar is not None:
                if self.pbar_desc_mode == 'filename':
                    self.pbar.set_description(self.current_img_filename)
                elif self.pbar_desc_mode == 'index':
                    self.pbar.set_description(str(self.n - 1))
                else:
                    raise ValueError
                self.pbar.update()
            return img
        else:
            if self.pbar is not None:
                self.pbar.close()
            raise StopIteration
    
    @classmethod
    def from_dir(
        self, img_dir: str, check_paths: bool=True,
        show_pbar: bool=False, leave_pbar: bool=False,
        pbar_desc_mode: str='filename'
    ) -> ImageIterator:
        if not isinstance(img_dir, str):
            raise TypeError(f"img_dir must be a str. Encountered {type(img_dir).__name__}")
        if not dir_exists(img_dir):
            raise FileNotFoundError(f"Couldn't find img_dir: {img_dir}")
        img_paths = get_valid_image_paths(img_dir)
        return ImageIterator(
            img_paths=img_paths, check_paths=check_paths,
            show_pbar=show_pbar, leave_pbar=leave_pbar,
            pbar_desc_mode=pbar_desc_mode
        )
