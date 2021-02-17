"""
    Module controlling YAML and hdf5 output files
"""
import yaml
import h5py
import hdfdict
import os

__all__ = ["write_dict_to_yaml","write_h5"]


def write_dict_to_yaml(dict_, out_name_, setindent = 2):
    """ Generic function writin a dictionary as a yaml file

        Input:
            :dict_: dictionary to write out as yaml
            :out_name_: output name of the .yml file
            :setindent: indentation setting of yaml file
        Output:
            a YAML file
    """
    with open(out_name_+'.yml', 'w') as yaml_out:
        yaml.dump(dict_, yaml_out, indent = setindent)


def write_h5(dict_, save_name_ = 'dump', save_path_='./'):
    tmp_dir = os.getcwd()
    if not os.path.exists(save_path_):
        os.makedirs(save_path_)
    os.chdir(save_path_)
    with h5py.File(save_name_ + ".h5", "w") as fout:
        hdfdict.dump(dict_, fout, lazy=False)
    os.chdir(tmp_dir)
    