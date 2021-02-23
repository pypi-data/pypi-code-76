"""Functions to download latest SICOR tables, also download links."""
import os
from glob import glob
import shutil
import sys
import json
import requests
import hashlib
from pkg_resources import resource_filename, Requirement, DistributionNotFound

from ..options import python_to_json
from .. import get_options
from .. import options
from .. import tables

# all paths within this set are searched for sicor tables

tables_origins = []

try:
    pp = resource_filename(Requirement.parse('sicor'), "data")
    if os.path.isdir(pp):
        tables_origins += [pp]
except DistributionNotFound:
    pass


tables_origins += list(set(sys.path))
# download url's for sicor tables, used as fallback if files are not found within tables_origins
sicor_downloads = {
    "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5":
        ("google_drive", "0B2ygRjmN4hzNcC15Z2pPS2tQdTg"),
    "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5":
        ("google_drive", "0B2ygRjmN4hzNRzhKZ3Z2V2FsWHM"),
    "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl":
        ("google_drive", "0B2ygRjmN4hzNSHN2RG1lY0M4RW8")
}

sicor_downloads_optional = {
    "ch4": {
        "fn": "linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5",
        "dn": ("google_drive", "0B2ygRjmN4hzNNEVmX29ROHhJTGc",)},
    "hyperspectral_sample": {
        "fn": "hyperspectral_sample.hdf5",
        "dn": ("google_drive", "0B2ygRjmN4hzNemk2OWtOQ3k4Rkk")},
    "s2_manual_classification": {
        "fn": "20170523_s2_manual_classification_data.h5",
        "dn": ("google_drive", "0B2ygRjmN4hzNXy0tckl3UkROSjg")
    },
}

file_checksums = {
    "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5":
        "b6d5189a694f25fe20f1ad664d465bcc",
    "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5":
        "aaf6da6c4a4286500407c04e0feb043a",
    "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl":
        "d2e14b204ac7ee486a946a1c3bded467",
    "linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5":
        "07bac6ff6cb6f927cffaeed297f94a54",
    "hyperspectral_sample.hdf5":
        "1ac7a3759a8ca1ae31a01832f5b7a418",
    "20170523_s2_manual_classification_data.h5":
        "d0a7b0c13b02d6da0ce60ac6ca9d29a2"
}


def verify_table(fn: str):
    """Check md5 sum os file fn

    :param fn:
    :return: None
    :raises: ValuError if fn of file is other than given in file_checksums
    """
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    if os.path.basename(fn) in file_checksums:
        md5sum_is = md5(fn)
        md5sum_should = file_checksums[os.path.basename(fn)]
        if md5sum_should != md5sum_is:
            raise ValueError("Md5Sum of file: {fn} is: {md5sum_is}, but should be: {md5sum_should}".format(
                fn=fn, md5sum_is=md5sum_is, md5sum_should=md5sum_should))


def get_tables(sicor_table_path=None, sensor="s2", style="link", optional_downloads=None, export_options_to=None):
    """
    Get LUT tables needed for SICOR. This function tries to automatically acquire the files. Tables are searched for in
    sys.path which includes the installations defaults and the $PYTHONPATH from the environment.

    :param sensor: sensor string from ["s2", "l8", "enmap"]
    :param sicor_table_path: None or path where to store SICOR tables, if "None", tables are stored within sicor.tables.
    :param style: either: "link": try to make symbolic link or "copy": copy LUT files
    :param optional_downloads: either None or iterable of strings such as : ("ch4",)
    :param export_options_to:
        None: export user options to: ./sicor_s2_user_options.json
        [filename]: If filename is given, export options to [filename], should be json
    :return: None
    :raises: ValueError if tables are not present after all attempts to acquire them.
    """

    if sensor == "enmap":
        settings = os.path.join(os.path.dirname(options.__file__), "{sensor}_options_old.json".format(sensor=sensor))
    else:
        settings = os.path.join(os.path.dirname(options.__file__), "{sensor}_options.json".format(sensor=sensor))
    opts = get_options(settings)
    sicor_tables = set([op['atm_tables_fn'] for scat_type, op in opts["RTFO"].items()] +
                       [opts['cld_mask']["persistence_file"], opts['cld_mask']["novelty_detector"]])
    sicor_tables_fn = {os.path.basename(fn) for fn in sicor_tables}  # sicor tables, only basename of path in opts

    if optional_downloads is not None:
        for opt_dn in optional_downloads:
            try:
                fn = str(sicor_downloads_optional[opt_dn]["fn"])
            except KeyError:
                print("Optional download: %s is not available" % opt_dn)
                raise

            sicor_tables_fn.update({fn})
            sicor_downloads[fn] = sicor_downloads_optional[opt_dn]["dn"]

    if sicor_table_path is None:
        sicor_table_path = os.path.dirname(tables.__file__)
    tables_origins.append(sicor_table_path)

    fn_table_paths = {}
    for fn_table in sicor_tables_fn:
        if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:  # is file already in sicor_table_path ?
            for table_path in tables_origins:  # look in predefined paths for files
                if os.path.isdir(table_path):
                    glb = glob(os.path.join(table_path, "**", fn_table), recursive=True)
                    if len(list(glb)) > 0:  # a file with the right name was found
                        if style == "link":
                            if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
                                os.symlink(glb[0], os.path.join(sicor_table_path, fn_table))
                                print("Make link file: %s" % glb[0])
                                fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)
                        elif style == "copy":
                            if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
                                print("Copy file: %s" % glb[0])
                                shutil.copy(glb[0], sicor_table_path)
                                fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)
        else:
            print("Table %s is already available in %s." % (fn_table, sicor_table_path))
            fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)

        if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
            print("File: %s not found locally, try to download." % fn_table)
            try:
                download_type, download = sicor_downloads[fn_table]
                if download_type == "google_drive":
                    print("Downloading %s from google drive: %s" % (fn_table, download))
                    download_file_from_google_drive(download, os.path.join(sicor_table_path, fn_table))
                    fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)
                else:
                    raise ValueError("Download type: %s is not implemented" % download_type)

            except KeyError:
                print("Table %s not available for download." % fn_table)
                raise ValueError("Table: %s unable to retrieve -> giving up." % fn_table)

    for fn_table, fn in fn_table_paths.items():
        verify_table(fn)

    def update_opts(opt):
        """
        if opt_v is string which contains a path to a sicor table, update path to the current sicor_table_path,
        if not return the string. If opt_v is dict, then recurse into key, value pairs and apply update_opts
        :param opt:
        :return:
        """
        if isinstance(opt, dict):
            return {k: update_opts(v) for k, v in opt.items()}
        elif isinstance(opt, str):
            for fn in sicor_tables_fn:
                if fn in opt:
                    return os.path.join(sicor_table_path, fn)
            return opt
        else:
            return opt

    new_opts = update_opts(opts)

    if export_options_to is None:
        opts_fn = os.path.join(os.path.dirname(options.__file__), "sicor_{sensor}_user_options.json".format(
            sensor=sensor))
    else:
        os.makedirs(os.path.dirname(export_options_to), exist_ok=True)
        opts_fn = export_options_to

    with open(opts_fn, "w") as fl:
        json.dump(python_to_json(new_opts), fl, indent=4)


def download_file_from_google_drive(gid, destination):
    """Download from gdrive using public id (gid)."""
    def get_confirm_token(response):
        """Get token from gdrive."""
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        """Get response from gdrive to file system."""
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com"
    session = requests.Session()
    response = session.get(URL, params={'id': gid}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': gid, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)
