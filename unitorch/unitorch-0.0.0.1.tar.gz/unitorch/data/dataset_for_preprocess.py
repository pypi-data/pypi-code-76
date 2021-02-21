import re
from torch.utils import data
from unitorch.core import core_class
from unitorch import core_process
from unitorch.data.dataset_for_raw_data import dataset_hf_from_file, dataset_hf_from_hub
from unitorch.functions import parser_process_function

NET_INPUTS_KEYS = set()
NET_TARGETS_KEYS = set()


def add_key_group_info(name, net_inputs=[], net_targets=[]):
    NET_INPUTS_KEYS.update(set(f"{name}/{key}" for key in net_inputs))
    NET_TARGETS_KEYS.update(set(f"{name}/{key}" for key in net_targets))


def merge_dicts_from_process(*args):
    ret_dict = dict()
    num_args = len(args)
    for i in range(num_args):
        keys = list(ret_dict.keys() & args[i].keys())
        nums = [1] * len(keys)
        for k in keys:
            ret_dict[f"{k}_a"]
        for j in range(i, num_args):
            for p, k in enumerate(keys):
                if k in args[j].keys():
                    args[j][f"{k}_{chr(nums[p] + 97)}"] = args[j].pop(k)
                    nums[p] += 1
        ret_dict.update(args[i])
    return ret_dict


class dataset_for_preprocess(data.Dataset):
    def __init__(
        self,
        data_dir=None,
        data_files=[],
        names=None,
        sep="\t",
        file_type="csv",
        data_name=None,
        split="train",
        preprocess_funcs=[],
    ):
        """
        Args:
        preprocess_funcs: [ 'process_func1(param1, param2, param3=value1)', 'process_func2(param1=value1)' ]
        """
        if data_name is not None:
            self._dataset = dataset_hf_from_hub(data_name=data_name, split=split)
        else:
            self._dataset = dataset_hf_from_file(
                data_dir=data_dir,
                data_files=data_files,
                names=names,
                sep=sep,
                file_type=file_type,
                split=split,
            )

        self.preprocess_funcs = []
        self._functions = []
        for precess_func_str in preprocess_funcs:
            func_infos = parser_process_function(precess_func_str)
            function = func_infos.pop("function")
            self._functions.append(function)
            if function not in core_process:
                raise f"can't find {function} in core_process"
            func_infos["function"] = core_process.get(function)
            self.preprocess_funcs.append(func_infos)

    @property
    def dataset(self):
        return self._dataset

    @staticmethod
    def get_new_args_kwargs(args, kwargs, row_dict):
        new_args = [row_dict[arg] if arg in row_dict else eval(arg) for arg in args]
        new_kwargs = dict(
            {k: row_dict[v] if v in row_dict else eval(v) for k, v in kwargs.items()}
        )
        return new_args, new_kwargs

    @staticmethod
    def get_net_inputs_targets(ret_dict, _function):
        inputs, targets = dict(), dict()
        for k, v in ret_dict.items():
            if k.startswith("net_inputs/"):
                inputs[k[11:]] = v
            elif k.startswith("net_targets/"):
                targets[k[12:]] = v
            elif f"{_function}/{k}" in NET_INPUTS_KEYS:
                inputs[k] = v
            elif f"{_function}/{k}" in NET_TARGETS_KEYS:
                targets[k] = v
            else:
                raise f"{_function}/{k} is net_inputs or net_targets ?"
        return inputs, targets

    def __getitem__(self, idx):
        row_dict = self.dataset[idx]
        ret_dict_list = []
        for precess_func in self.preprocess_funcs:
            old_args, old_kwargs = precess_func.get("args"), precess_func.get("kwargs")
            new_args, new_kwargs = self.get_new_args_kwargs(
                old_args, old_kwargs, row_dict
            )
            ret_dict_list.append(precess_func.get("function")(*new_args, **new_kwargs))

        net_inputs_targets = [
            self.get_net_inputs_targets(ret, self._functions[i])
            for i, ret in enumerate(ret_dict_list)
        ]
        net_inputs, net_targets = zip(*net_inputs_targets)
        net_inputs = merge_dicts_from_process(*net_inputs)
        net_targets = merge_dicts_from_process(*net_targets)
        ret_dict = dict(
            {
                "net_inputs": net_inputs,
                "net_targets": net_targets,
            }
        )
        return ret_dict

    def __len__(self):
        return len(self._dataset)
