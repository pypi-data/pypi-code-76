"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import gc
import os
import unicodedata

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.misc import datetime_isoformat_to_discord_format
from antipetros_discordbot.utility.gidtools_functions import (readit, clearit, readbin, work_in, writeit, loadjson, pickleit, splitoff, writebin, pathmaker, writejson, dir_change,
                                                              linereadit, bytes2human, create_file, file_walker, get_pickled, ishash_same, ext_splitter, appendwriteit, create_folder,
                                                              number_rename, timenamemaker, cascade_rename, file_name_time, absolute_listdir, hash_to_solidcfg, path_part_remove,
                                                              from_dict_to_file, get_absolute_path, file_name_modifier, limit_amount_of_files, limit_amount_files_absolute)
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class EmbedFactory:

    def __inti__(self):
        pass


# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
