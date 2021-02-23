import os
from typing import Iterable, Set, Tuple, Union

import numpy as np

from continuum import download
from continuum.datasets.base import _ContinuumDataset


class _SemanticSegmentationDataset(_ContinuumDataset):
    @property
    def data_type(self) -> str:
        return "semantic_segmentation"


class PascalVOC2012(_SemanticSegmentationDataset):
    data_url = "http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar"
    segmentation_url = "http://cs.jhu.edu/~cxliu/data/SegmentationClassAug.zip"
    split_url = "http://cs.jhu.edu/~cxliu/data/list.zip"

    def __init__(self, data_path: str = "", download: bool = True) -> None:
        super().__init__(data_path, download)

    def _download(self):
        if not os.path.exists(os.path.join(self.data_path, "truc")):
            print("Downloading Pascal VOC dataset, it's slow!")
            download(self.data_url, self.data_path)
            # TODO untar

        if not os.path.exists(os.path.join(self.data_path, "SegmentationClassAug.zip")):
            path = download.download(self.segmentation_url, self.data_path)
            download.unzip(path)
        if not os.path.exists(os.path.join(self.data_path, "list.zip")):
            path = download.download(self.split_url, self.data_path)
            download.unzip(path)

    def get_data(self, train: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if train:
            list_path = os.path.join(self.data_path, "list", "train_aug.txt")
        else:
            list_path = os.path.join(self.data_path, "list", "val.txt")

        image_paths, map_paths = [], []
        with open(list_path, "r") as f:
            for line in f:
                p1, p2 = line.split(" ")
                image_paths.append(os.path.join(self.data_path, "VOCdevkit", "VOC2012", p1))
                map_paths.append(os.path.join(self.data_path, p2))

        return np.array(image_paths), np.array(map_paths), None
