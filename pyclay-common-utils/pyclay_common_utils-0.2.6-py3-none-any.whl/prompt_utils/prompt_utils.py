import sys
from logger import logger
from ..adv_file_utils import delete_all_files_in_extension_list
from ..file_utils import delete_dir

def standard_prompt() -> bool:
    answer = input('yes/no: ')
    if answer.lower() in ['y', 'yes']:
        consent = True
    elif answer.lower() in ['n', 'no']:
        consent = False
    else:
        logger.error(f"Invalid response: {answer}")
        raise Exception
    return consent

def terminate_on_no_prompt() -> bool:
    if standard_prompt():
        return True
    else:
        logger.warning("Terminating program.")
        sys.exit()

def delete_files_in_dir_prompt(dir_path: str, extension_list: list):
    if terminate_on_no_prompt():
        delete_all_files_in_extension_list(dir_path=dir_path, extension_list=extension_list)

def delete_dir_prompt(dir_path: str):
    if terminate_on_no_prompt():
        delete_dir(dir_path=dir_path)

def weights_scratch_prompt() -> bool:
    logger.warning(f"Would you like to start from scratch?")
    if terminate_on_no_prompt():
        return True

def weights_newest_prompt(newest_weights_path: str) -> bool:
    logger.warning(f"Would you like to resume from the newest weights path?\n{newest_weights_path}")
    return standard_prompt()