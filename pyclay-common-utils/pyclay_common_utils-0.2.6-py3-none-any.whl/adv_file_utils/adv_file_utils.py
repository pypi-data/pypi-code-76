from ..file_utils import move_file, delete_existing_file
from ..path_utils import get_next_dump_path, get_extension_from_path, \
    get_pathlist, get_all_files_of_extension, get_filename, get_all_files_in_extension_list
from ..file_utils import file_exists, dir_exists

def move_to_dump_dir(
    src_path: str, dump_dir: str, label_length: int=6,
    silent: bool=False
    ):
    file_extension = get_extension_from_path(src_path)
    dump_path = get_next_dump_path(
        dump_dir=dump_dir,
        file_extension=file_extension,
        label_length=label_length,
        starting_number=0,
        increment=1
    )
    move_file(src_path=src_path, dest_path=dump_path, silent=silent)

def move_all_to_dump_dir(
    src_dir: str, dump_dir: str, label_length: int=6,
    silent: bool=False
    ):
    src_pathlist = get_pathlist(src_dir)
    for src_path in src_pathlist:
        move_to_dump_dir(
            src_path=src_path,
            dump_dir=dump_dir,
            label_length=label_length,
            silent=silent
        )

def delete_all_files_of_extension(dir_path: str, extension: str):
    filepaths = get_all_files_of_extension(dir_path, extension)
    if len(filepaths) > 0:
        for filepath in filepaths:
            delete_existing_file(filepath)
            print(f'Deleted {filepath}')

def delete_all_files_in_extension_list(dir_path: str, extension_list: list):
    filepaths = get_all_files_in_extension_list(dir_path, extension_list)
    if len(filepaths) > 0:
        for filepath in filepaths:
            delete_existing_file(filepath)
            print(f'Deleted {filepath}')

def get_filepaths_in_dir(dir_path: str):
    pathlist = get_pathlist(dir_path)
    filepaths_in_dir = []
    for path in pathlist:
        if file_exists(path):
            filepaths_in_dir.append(path)
    return filepaths_in_dir

def get_filenames_in_dir(dir_path: str):
    filepaths_in_dir = get_filepaths_in_dir(dir_path)
    return [get_filename(filepath) for filepath in filepaths_in_dir]

def get_dirpaths_in_dir(dir_path: str):
    pathlist = get_pathlist(dir_path)
    dirpaths_in_dir = []
    for path in pathlist:
        if dir_exists(path):
            dirpaths_in_dir.append(path)
    return dirpaths_in_dir

def get_dirnames_in_dir(dir_path: str):
    dirpaths_in_dir = get_dirpaths_in_dir(dir_path)
    return [get_filename(dirpath) for dirpath in dirpaths_in_dir]