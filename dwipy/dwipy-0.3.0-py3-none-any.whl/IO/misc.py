import os
import tempfile
import glob


def get_file_base_name_without_extension(file_path):
    file_path = os.path.normpath(file_path)
    file_name = os.path.basename(file_path)

    return file_name.split(".")[0]


def _get_tmp_dir():
    return tempfile.mkdtemp()


def get_number_of_dcm_files(dicom_folder):
    return len(glob.glob(os.path.join(dicom_folder, "*.dcm")))
