import os
from functools import partial
from torch.utils import data
from datasets import load_dataset, list_datasets
from datasets import Dataset

list_datasets_from_hub = list_datasets()


def load_csv(data_dir, data_files, sep=",", names=None):
    return load_dataset(
        "csv",
        data_dir=data_dir,
        data_files=data_files,
        delimiter=sep,
        column_names=names,
        quoting=3,
    )


def load_json(data_dir, data_files, field=None):
    return load_dataset("json", data_dir=data_dir, data_files=data_files, field=field)


def is_file_available(fpath, data_dir=None):
    if data_dir is None:
        return os.path.exists(fpath)
    return os.path.exists(os.path.join(data_dir, fpath))


class dataset_hf_from_file(data.Dataset):
    def __init__(
        self,
        data_dir=None,
        data_files=[],
        names=None,
        sep="\t",
        file_type="csv",
        split="train",
    ):

        data_files = [f for f in data_files if is_file_available(f, data_dir)]
        assert len(data_files) > 0
        load_func = (
            load_json
            if file_type == "json"
            else partial(load_csv, sep=sep, names=names)
        )
        self._dataset = load_func(data_dir, dict({split: data_files})).get(split)
        assert isinstance(self._dataset, Dataset)

    @property
    def dataset(self):
        return self._dataset

    def __getitem__(self, idx):
        return self._dataset[idx]

    def __len__(self):
        return len(self._dataset)


class dataset_hf_from_hub(data.Dataset):
    def __init__(
        self,
        data_name,
        split=None,
    ):

        assert data_name in list_datasets_from_hub
        split = "validation" if split == "dev" else split
        self._dataset = load_dataset(data_name, split=split)
        assert isinstance(self._dataset, Dataset)

    @property
    def dataset(self):
        return self._dataset

    def __getitem__(self, idx):
        return self._dataset[idx]

    def __len__(self):
        return len(self._dataset)


class dataset_for_large_file(data.Dataset):
    pass
