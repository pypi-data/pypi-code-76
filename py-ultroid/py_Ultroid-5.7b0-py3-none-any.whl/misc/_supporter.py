# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# For Other USERBOTs plugin Support

from telethon.tl.types import ChatBannedRights
import os
from .. import *
from ..utils import *
from pyUltroid.misc._decorators import *
import re
import inspect
import functools
from ..functions.sudos import *
from telethon import *
from plugins import *
from ..dB.database import Var
from ..dB.core import *
from pathlib import Path
from sys import *


CMD_HELP = {}

ALIVE_NAME = OWNER_NAME
BOTLOG = Var.LOG_CHANNEL
BOTLOG_CHATID = Var.LOG_CHANNEL


bot = ultroid_bot
borg = ultroid_bot
friday = ultroid_bot
jarvis = ultroid_bot

ok = udB.get("SUDOS")
if ok:
    SUDO_USERS = set(int(x) for x in ok.split())
else:
    SUDO_USERS = ""

if SUDO_USERS:
    sudos = list(SUDO_USERS)
else:
    sudos = ""

hndlr = "\\" + Var.HNDLR if Var.HNDLR is not None else "."


def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except:
                pass
            try:
                LIST[file_test].append(cmd)
            except:
                LIST.update({file_test: [cmd]})
        except:
            pass
    args["outgoing"] = True
    if "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    args["blacklist_chats"] = True
    black_list_chats = list(Var.BLACKLIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return events.NewMessage(**args)


friday_on_cmd = admin_cmd
j_cmd = admin_cmd
command = ultroid_cmd
register = ultroid_cmd


def sudo_cmd(allow_sudo=True, pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
    if allow_sudo:
        args["from_users"] = SUDO_USERS
        args["incoming"] = True
    args["blacklist_chats"] = True
    black_list_chats = list(Var.BLACKLIST_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return events.NewMessage(**args)


def sudo():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id == ultroid_bot.uid or is_sudo(event.sender_id):
                await function(event)
            else:
                pass
        return wrapper
    return decorator


async def eor(event, text):
    if is_sudo(event.sender_id):
        reply_to = await event.get_reply_message()
        if reply_to:
            return await reply_to.reply(text)
        return await event.reply(text)
    return await event.edit(text)