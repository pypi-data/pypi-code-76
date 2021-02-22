import shutil
import glob
import os

from .constants import (
    CWD,
    DEFAULT_DATA_DIR,
    USER_PATH,
    MODULE_DATA_PATH,
    WEATHER_FILES,
)


def find_files_oswalk(root, templates_search_dir, search=None):
    for file in glob.glob(
        os.path.join(root, templates_search_dir, "**/*.*"), recursive=True
    ):
        exists = False
        section = ""
        basefile = os.path.basename(file)
        inbetween = file[len(root) + 1 : -len(basefile) - 1].split(os.sep)
        newsection = inbetween[:]
        if search is not None:
            if search in inbetween:
                exists = True
                newsection.remove(search)
            if templates_search_dir in inbetween:
                newsection.remove(templates_search_dir)
        if newsection:
            section = os.path.join(*newsection)
        yield (file, root, section, basefile, exists)


def copy_to_user_data_dir(location=None):
    user_dir = location or USER_PATH or DEFAULT_DATA_DIR
    os.makedirs(user_dir, exist_ok=True)
    PKG_DATA_FILES = glob.glob(os.path.join(MODULE_DATA_PATH, "*.*"))
    for file in PKG_DATA_FILES:
        basefile = os.path.basename(file)
        if basefile in WEATHER_FILES.keys():
            rest = file.rsplit(MODULE_DATA_PATH)[-1][1:]
            base = rest.rsplit(basefile)[0][:-1]
            destpath = os.path.join(user_dir, base, WEATHER_FILES[basefile])
            if not os.path.exists(destpath):
                print(destpath)
                os.makedirs(os.path.split(destpath)[0], exist_ok=True)
                shutil.copyfile(file, destpath)
        else:
            rest = file.rsplit(MODULE_DATA_PATH)[-1][1:]
            destpath = os.path.join(user_dir, rest)
            if not os.path.exists(destpath):
                print(destpath)
                os.makedirs(os.path.split(destpath)[0], exist_ok=True)
                shutil.copyfile(file, destpath)


def create_project(project_name, template):
    template_check = ["base", "eg1", "eg2", "eg3"]
    if template in template_check:
        pass
    else:
        raise Exception(
            f"--template argument '{template}' not in {' '.join(template_check)}"
        )

    template_dir_path = os.path.join(MODULE_DATA_PATH, template)
    if not os.path.exists(template_dir_path):
        raise Exception(
            f"Directory '{template_dir_path}' does not exist. Make sure you call copy_to_user_data_dir function first"
        )

    print(f"Copy files from {template_dir_path}")
    for file, _, section, basefile, _ in find_files_oswalk(template_dir_path, ""):
        destination_file_abspath = os.path.join(CWD, project_name, section, basefile)
        os.makedirs(os.path.split(destination_file_abspath)[0], exist_ok=True)
        shutil.copyfile(file, destination_file_abspath)
        print(f"   {destination_file_abspath}")
    print("Done!")
    return None
