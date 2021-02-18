import logging
import subprocess
import traceback
import os
import zipfile
import configparser

FORMAT = "%(asctime)s|%(levelname)s|%(message)s"
logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO, format=FORMAT)

config = configparser.ConfigParser()
config_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], "config.ini")
config.read(config_path)


class ScanType:
    SOURCE_CODE = "source_code"
    BINARY = "binary"


def error_exit(msg):
    logger.error(msg)
    exit(1)


def exec_command(cmd, work_dir="."):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work_dir
    )
    try:
        out, err = p.communicate()
        if err:
            return {"error": err, "output": out.strip()}
    except Exception as e:
        return {"error": traceback.format_exc()}
    return {"output": out.strip()}


def zip_folder(folderpath):
    def _zipdir(folderpath, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(folderpath):
            for file in files:
                ziph.write(os.path.join(root, file))

    tail_path, basename = os.path.split(folderpath)
    zipfilename = os.path.join(tail_path, "%s.zip" % basename)
    zipf = zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED)
    _zipdir(folderpath, zipf)
    zipf.close()
    return zipfilename


# def read_paths(file_path):
#     path_list = []
#     with open(file_path, "r") as fp:
#         paths = fp.readlines()
#         if not os.path.exists(os.path.join(os.curdir, "projects")):
#             os.mkdir(os.path.join(os.curdir, "projects"))
#         base_dest = os.path.join(os.getcwd(), "projects")
#         for path in paths:
#             file = zipfile.ZipFile(path.replace("\n", ""), "r")
#             file_name = os.path.split(file.filename)[-1]
#             dest = os.path.join(base_dest, file_name.replace(".zip", ""))
#             if os.path.exists(dest):
#                 shutil.rmtree(dest)
#             os.mkdir(dest)
#             file.extractall(dest)
#             path_list.append(dest)
#         fp.close()
#     return path_list


def set_config(block, key, value):
    config.set(block, key, value)

    with open(config_path, 'w') as configfile:
        config.write(configfile)


def get_upload_zip_file(path):
    # create new scan and upload local file
    if os.path.isfile(path):
        file = path
    elif os.path.isdir(path):
        file = zip_folder(path)
    else:
        error_exit("Please provide a valid file path")

    return file


def debug_logger_level():
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
