"""
Abstract class representing a generic Dataset.
"""
from abc import abstractmethod
from pathlib import Path
from typing import Callable, List

from torch.utils.data import Dataset as PyTDataset


class Dataset(PyTDataset):
    """Abstract Class representing a generic dataset.

    Args:
        path_root: The path to the folder containing the dataset.
        split: The name of the split to load.
        loader: The function to load the point cloud. Defaults to np.loadtxt.
        download: If true download the dataset from url. Defaults to False.
        transforms (optional): The transform to apply to the item. Defaults to [].

    Raises:
        ValueError in the split is not in: train, val or test.
    """

    def __init__(
        self,
        path_root: Path,
        split: str,
        download: bool = False,
        transforms: List[Callable] = [],
    ) -> None:

        self.path_root = path_root
        self.samples: List = []
        self.split = split
        self.transforms = transforms

        splits = ["train", "val", "test"]
        if split not in splits:
            raise ValueError((f"Split {split} found, but expected either " "train, val, or test"))

        if download is True:
            self.download()

    def __len__(self) -> int:
        """Get the lenght of the dataset.

        Returns:
            The number of samples in the dataset.
        """
        return len(self.samples)

    @abstractmethod
    def download(self) -> None:
        """Function to download the compressed dataset."""
        raise NotImplementedError("Function not implemented.")
