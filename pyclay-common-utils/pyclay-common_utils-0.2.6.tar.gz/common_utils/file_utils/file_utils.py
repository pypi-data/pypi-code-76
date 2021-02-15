import os, sys, subprocess
from shutil import rmtree, copyfile
from distutils.dir_util import copy_tree

from logger import logger

def dir_exists(url: str):
    return os.path.isdir(url)

def file_exists(url: str):
    return os.path.isfile(url)

def link_exists(url: str):
    return os.path.islink(url)

def delete_file(url: str):
    os.unlink(url)

def delete_existing_file(url: str):
    if file_exists(url):
        delete_file(url)
    else:
        logger.error(f"Error: Failed to delete {url}. File doesn't exist.")
        raise Exception

def delete_file_if_exists(url: str):
    if file_exists(url):
        delete_file(url)

def delete_dir(dir_path: str):
    rmtree(dir_path)

def delete_existing_dir(url: str):
    if dir_exists(url):
        delete_dir(url)
    else:
        logger.error(f"Error: Failed to delete {url}. Directory doesn't exist.")
        raise Exception

def delete_dir_if_exists(url: str):
    if dir_exists(url):
        delete_dir(url)

def make_dir(dir_path: str):
    os.mkdir(dir_path)

def make_dir_if_not_exists(dir_path: str):
    if not dir_exists(dir_path):
        make_dir(dir_path)

def get_dir_contents_len(dir_path: str) -> int:
    return len(os.listdir(dir_path))

def dir_is_empty(dir_path: str) -> bool:
    return get_dir_contents_len(dir_path) == 0

def delete_all_files_in_dir(dir_path: str, ask_permission: bool=True, verbose: bool=False):
    if not dir_is_empty(dir_path):
        if ask_permission:
            logger.warning(f'Are you sure that you want to delete all of the files in {dir_path}?')
            consent = input('yes/no: ')
            if consent != 'yes':
                logger.warning('Program terminated')
                sys.exit()
        names = os.listdir(dir_path)
        for name in names:
            path = os.path.join(dir_path, name)
            if file_exists(path):
                delete_file(path)
            else:
                delete_dir(path)
            if verbose:
                logger.info('Deleted {}'.format(path.split('/')[-1]))
    else:
        if verbose:
            logger.warning('Directory is empty. Nothing to delete.')

def init_dir(dir_path: str, ask_permission: bool=True):
    dir_name = dir_path.split('/')[-1]
    if not dir_exists(dir_path):
        make_dir(dir_path)
        logger.info("Created directory {}".format(dir_name))
    else:
        delete_all_files_in_dir(dir_path, ask_permission)
        logger.info("All files have been deleted from directory {}".format(dir_name))
    logger.good('Directory {} has been initialized'.format(dir_name))

def copy_file(src_path: str, dest_path: str, silent: bool=False):
    copyfile(src_path, dest_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        logger.info('Copied {} to {}'.format(src_preview, dest_preview))

def copy_dir(src_path: str, dest_path: str, silent: bool=False):
    copy_tree(src_path, dest_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        logger.info('Copied {} to {}'.format(src_preview, dest_preview))

def move_file(src_path: str, dest_path: str, silent: bool=False):
    copy_file(src_path, dest_path, silent=True)
    delete_file(src_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        logger.info('Moved {} to {}'.format(src_preview, dest_preview))

def move_dir(src_path: str, dest_path: str, silent: bool=False):
    copy_dir(src_path, dest_path, silent=True)
    delete_dir(src_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        logger.info('Moved {} to {}'.format(src_preview, dest_preview))

def create_softlink(src_path: str, dst_path: str):
    if link_exists(dst_path):
        delete_file(dst_path)
    subprocess.run(f"ln -s '{src_path}' '{dst_path}'", shell=True)
