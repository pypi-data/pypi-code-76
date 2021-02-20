"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import gc
import os
import unicodedata

# * Third Party Imports --------------------------------------------------------------------------------->
import aiohttp
import discord
from discord import File, Embed, DiscordException
from discord.ext import tasks, commands
from async_property import async_property

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.named_tuples import MemberRoleItem
from antipetros_discordbot.utility.gidtools_functions import (readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson, dir_change,
                                                              linereadit, create_file, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
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


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
