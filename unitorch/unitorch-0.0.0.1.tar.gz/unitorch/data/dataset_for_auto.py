import os
from torch.utils import data
from unitorch import register_dataset
from unitorch.data.dataset_for_preprocess import dataset_for_preprocess


@register_dataset("core/dataset/auto")
class dataset_for_auto_configure(data.Dataset):
    def __init__(
        self,
        data_dir=None,
        data_files=dict(),
        names=dict(),
        data_name=None,
        preprocess_funcs=dict(),
    ):
        self._dataset = {
            split: dataset_for_preprocess(
                data_dir=data_dir,
                data_files=data_files.get(split),
                names=names.get(split),
                data_name=data_name,
                preprocess_funcs=preprocess_funcs.get(split),
                split=split,
            )
            for split in ["train", "dev", "test"]
            if data_name is not None or data_files.get(split) is not None
        }

    def get(self, split):
        return self._dataset.get(split)

    @classmethod
    def init_from_core_configure(cls, cfg, **kwargs):
        data_dir = cfg.getdefault("core/dataset", "data_dir", None)
        data_files = cfg.getdefault("core/dataset", "data_files", None)
        data_files_dir = cfg.getdefault("core/dataset", "data_files_dir", None)
        names = cfg.getdefault("core/dataset", "names", None)
        data_name = cfg.getdefault("core/dataset", "data_name", None)
        preprocess_funcs = cfg.getdefault("core/dataset", "preprocess_funcs", None)

        data_files_group, names_group, preprocess_funcs_group = (
            dict(),
            dict(),
            dict(),
        )
        for split in ["train", "dev", "test"]:
            _data_files_dir = cfg.getdefault(
                f"core/dataset/{split}", "data_files_dir", data_files_dir
            )
            _data_files = cfg.getdefault(
                f"core/dataset/{split}", "data_files", data_files
            )
            _names = cfg.getdefault(f"core/dataset/{split}", "names", names)
            _preprocess_funcs = cfg.getdefault(
                f"core/dataset/{split}", "preprocess_funcs", preprocess_funcs
            )
            if _names is not None:
                _names = _names.split(",")

            if _data_files is not None:
                _data_files = list(map(lambda x: x.strip(), _data_files.split(",")))

            if _data_files_dir is not None and _data_files is not None:
                _data_files = [os.path.join(_data_files_dir, f) for f in _data_files]

            if _preprocess_funcs is not None:
                _preprocess_funcs = eval(_preprocess_funcs)
                preprocess_funcs_group[split] = _preprocess_funcs

            if _data_files is not None:
                data_files_group[split] = _data_files
                names_group[split] = _names

        return cls(
            data_dir=data_dir,
            data_files=data_files_group,
            names=names_group,
            data_name=data_name,
            preprocess_funcs=preprocess_funcs_group,
        )
