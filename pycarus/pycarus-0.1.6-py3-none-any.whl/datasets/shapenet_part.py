import json
import shutil
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np  # type: ignore
import open3d  # type: ignore
import torch

from pycarus.datasets.dataset import Dataset
from pycarus.geometry.pcd import color_point_cloud
from pycarus.utils import download_and_extract

T_ITEM = Tuple[torch.Tensor, int, torch.Tensor]
T_SAMPLES = List[Tuple[str, int]]


class ShapeNetPartSegmentation(Dataset):
    """Class representing the ShapeNet part segmentation dataset as presented in:

    Yi, Li, et al. "A scalable active framework for region annotation in 3d shape collections."
    ACM Transactions on Graphics (ToG) 35.6 (2016): 1-12.

    Args:
        path_root: The path to the folder containing the dataset.
        split: The name of the split to load.
        loader: The function to load the point cloud. Defaults to np.loadtxt.
        download: If True download the dataset from url, to download and extract the dataset
                  the 'tmp' folder is used. Defaults to False.
        transforms (optional): The transform to apply to the item. Defaults to [].

    Raises:
        ValueError in the split is not in: train, val or test.
    """

    url = "https://shapenet.cs.stanford.edu/media/shapenetcore_partanno_segmentation_benchmark_v0_normal.zip"
    md5_hash = "8c2f54f22c3f1d0e69da83b86f17f5ec"

    seg_part_to_label = {
        "02691156": [0, 1, 2, 3],
        "02773838": [4, 5],
        "02954340": [6, 7],
        "02958343": [8, 9, 10, 11],
        "03001627": [12, 13, 14, 15],
        "03261776": [16, 17, 18],
        "03467517": [19, 20, 21],
        "03624134": [22, 23],
        "03636649": [24, 25, 26, 27],
        "03642806": [28, 29],
        "03790512": [30, 31, 32, 33, 34, 35],
        "03797390": [36, 37],
        "03948459": [38, 39, 40],
        "04099429": [41, 42, 43],
        "04225987": [44, 45, 46],
        "04379243": [47, 48, 49],
    }

    seg_label_to_color = torch.Tensor(
        [
            [0.65, 0.95, 0.05],
            [0.35, 0.05, 0.35],
            [0.65, 0.35, 0.65],
            [0.95, 0.95, 0.65],
            [0.95, 0.65, 0.05],
            [0.35, 0.05, 0.05],
            [0.65, 0.05, 0.05],
            [0.65, 0.35, 0.95],
            [0.05, 0.05, 0.65],
            [0.65, 0.05, 0.35],
            [0.05, 0.35, 0.35],
            [0.65, 0.65, 0.35],
            [0.35, 0.95, 0.05],
            [0.05, 0.35, 0.65],
            [0.95, 0.95, 0.35],
            [0.65, 0.65, 0.65],
            [0.95, 0.95, 0.05],
            [0.65, 0.35, 0.05],
            [0.35, 0.65, 0.05],
            [0.95, 0.65, 0.95],
            [0.95, 0.35, 0.65],
            [0.05, 0.65, 0.95],
            [0.65, 0.95, 0.65],
            [0.95, 0.35, 0.95],
            [0.05, 0.05, 0.95],
            [0.65, 0.05, 0.95],
            [0.65, 0.05, 0.65],
            [0.35, 0.35, 0.95],
            [0.95, 0.95, 0.95],
            [0.05, 0.05, 0.05],
            [0.05, 0.35, 0.95],
            [0.65, 0.95, 0.95],
            [0.95, 0.05, 0.05],
            [0.35, 0.95, 0.35],
            [0.05, 0.35, 0.05],
            [0.05, 0.65, 0.35],
            [0.05, 0.95, 0.05],
            [0.95, 0.65, 0.65],
            [0.35, 0.95, 0.95],
            [0.05, 0.95, 0.35],
            [0.95, 0.35, 0.05],
            [0.65, 0.35, 0.35],
            [0.35, 0.95, 0.65],
            [0.35, 0.35, 0.65],
            [0.65, 0.95, 0.35],
            [0.05, 0.95, 0.65],
            [0.65, 0.65, 0.95],
            [0.35, 0.05, 0.95],
            [0.35, 0.65, 0.95],
            [0.35, 0.05, 0.65],
        ]
    )

    def __init__(
        self,
        path_root: Path,
        split: str,
        download: bool = False,
        transforms: List[Callable] = [],
    ) -> None:

        super().__init__(path_root, split, download, transforms)
        self.path_file_split = (
            self.path_root
            / Path("train_test_split")
            / Path(f"shuffled_{self.split}_file_list.json")
        )
        classes, class_to_idx = self._get_classes(self.path_root)

        self.samples = self._get_samples(self.path_file_split, class_to_idx)
        self.targets = [s[1] for s in self.samples]
        self.classes = classes
        self.class_to_idx = class_to_idx
        self.ids_to_categories: Dict[str, str] = self._read_ids_to_categories_dict()

    def _read_ids_to_categories_dict(self) -> Dict[str, str]:
        """Read the synsetoffset2category file of ShapeNet dataset.

        Returns:
            A dictionary where the keys are the ids of the categories while the values the name.
        """
        result: Dict[str, str] = {}
        path_file_category = self.path_root / Path("synsetoffset2category.txt")
        with open(path_file_category) as reader:
            content = reader.readlines()
            for element in content:
                element_splitted = element.rstrip().split("\t")
                result[element_splitted[1]] = element_splitted[0]

        return result

    def _get_classes(self, path: Path) -> Tuple[List[str], Dict[str, int]]:
        """Get the classes for the dataset using the folders.

        Args:
            path: the path to the dataset.

        Returns:
            - The classes.
            - The class to index dictionary.
        """
        classes = [
            folder.name
            for folder in path.iterdir()
            if folder.is_dir() and folder.name != "train_test_split"
        ]
        classes.sort()
        class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}

        return classes, class_to_idx

    def _get_samples(self, path_file_split: Path, class_to_idx: Dict[str, int]) -> T_SAMPLES:
        """Get all the samples of the dataset.

        Args:
            path_file_split: path to the split file.
            class_to_idx: the class to label index dictionary.

        Returns:
            The name of the samples together with the class labels.
        """
        file_split = open(str(path_file_split), "r")
        list_samples = json.loads(file_split.read())
        samples: List[Tuple[str, int]] = []

        for sample in list_samples:
            sample_splits = sample.split("/")
            name_class = sample_splits[-2]
            name_sample = sample_splits[-1]
            label = class_to_idx[name_class]

            samples.append((name_sample, label))

        return samples

    def __getitem__(self, index: int) -> T_ITEM:
        """Get one sample.

        Args:
            index: The index of the requested element.

        Returns:
            - the point cloud as a torch tensor with shape (NUM_POINTS, D).
            - the class label.
            - the segmentation part labels with shape (NUM_POINTS, D).
        """
        name_sample, label = self.samples[index]
        name_category = self.classes[label]
        path_file_sample = self.path_root / Path(name_category, f"{name_sample}.txt")
        pcd_norm_label = np.array(np.loadtxt(str(path_file_sample)))
        pcd = torch.tensor(pcd_norm_label[:, 0:3], dtype=torch.float)
        parts_labels = torch.tensor(pcd_norm_label[:, -1], dtype=torch.long)

        return pcd, label, parts_labels

    def download(self) -> None:
        path_temp = Path("/tmp")
        path_file_downloaded = path_temp / Path(self.url.split("/")[-1])
        download_and_extract(self.url, path_file_downloaded, path_temp, self.md5_hash)

        path_ds_extracted = path_temp / Path(
            "shapenetcore_partanno_segmentation_benchmark_v0_normal"
        )

        shutil.copytree(str(path_ds_extracted), self.path_root)
        shutil.rmtree(str(path_ds_extracted))

    @classmethod
    def show_item(cls, sample: T_ITEM) -> open3d.geometry.PointCloud:
        """Prepare one item in order to be visualized using open3D draw geometries.

        Args:
            sample: The sample to show.

        Returns:
            The point cloud to draw with open 3D.
        """
        pcd, _, parts_labels = sample
        col = cls.seg_label_to_color[parts_labels, :]

        return color_point_cloud(pcd, col)
