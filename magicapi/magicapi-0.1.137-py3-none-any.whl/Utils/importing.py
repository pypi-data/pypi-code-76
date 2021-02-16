from os.path import dirname, basename, isfile, join, exists
import glob


def get_all_subfiles_and_dirs(file_name):

    # first get all of the python files
    modules = glob.glob(join(dirname(file_name), "*.py"))
    __all__v = [
        basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
    ]

    # now import all of the directories
    init = "__init__.py"
    dirs_with_init = glob.glob(join(dirname(file_name), f"*/{init}"))
    for dir_with_init in dirs_with_init:
        d = dir_with_init.replace(f"/{init}", "")
        __all__v.append(basename(d))

    return __all__v
