#! /usr/bin/env python3


import os
import re
import logging
import argparse
import datetime
import webbrowser
import subprocess
from pathlib import Path

from . import tools
from . import constants
from . fileoperator import FileOperator
from . streamerretriever import StreamerRetriever


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)

file_handler = logging.FileHandler(constants.CLI_LOG)
formatter = logging.Formatter(constants.CLI_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--version', help='show version', action='store_true')
    parser.add_argument(
        '-c', '--check', help='check online streams and output names',
        action='store_true')
    parser.add_argument(
        '-l', '--link', help='check online streams and output links',
        action='store_true')
    parser.add_argument(
        '-p', '--play', help='check streams and choose what to play',
        action='store_true')
    parser.add_argument(
        '-d', '--vod', help='check vods and choose what to play',
        action='store_true')
    parser.add_argument(
        '-w', '--web', help='use default webbrowser with play',
        action='store_true')
    parser.add_argument(
        '-m', '--mobile', help='make link into twitch mobile version',
        action='store_true')
    parser.add_argument(
        '-t', '--twitch-follows', help='print your follows from twitch',
        action='store_true')
    args = parser.parse_args()
    return args


def tokenInput():
    url = input()
    return url


def initStreamerRetriever():
    token = tools.oauth(tokenInput)
    streamerretriever = StreamerRetriever(token)
    return streamerretriever


def showVodInfo(value):
    def timeFormat():
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        time = datetime.datetime.strptime(value.getCreatedAt(), time_format)
        return time.strftime("%a, %d. %B %H:%M")

    title = value.getTitle()
    show_info = (
        f'{timeFormat()}, Duration: {value.getDuration()}\n' + ' ' * 5 +
        f'{title}' + '\n')
    return show_info


def showDispName(value):
    return value.getDispName()


def showAsk(listing, showInfo):
    for i, value in enumerate(listing):
        t = '{:<5}'.format(f'#{i+1}')
        print(f'{t}{showInfo(value)}')


def checkAsk():
    val = input('#')
    r = re.compile(r'^([1-9][0-9]*)$')
    match = r.match(val)
    return match


def getAsk(listing, match):
    choice = int(match.group())
    if choice <= len(listing):
        value = listing[choice-1]
        return value


def askInput(listing, showInfo):
    showAsk(listing, showInfo)
    match = checkAsk()
    if match:
        value = getAsk(listing, match)
        return value


def vodPrinting(name):
    space = ' ' * 5
    prefix = '#   '
    txt = ' - VODS'
    line = '#' * (len(name.getDispName()) + len(txt) + len(prefix) * 2)
    print()
    print(space + line)
    print(space + prefix + name.getDispName() + txt + prefix[::-1])
    print(space + line)


def getPlayer():
    base = constants.BASES[os.name]
    cli_conf = constants.CONFIG
    p = Path.resolve(Path.expanduser(Path(base)))
    path = p / cli_conf

    fo = FileOperator(str(path))
    configs = fo.loadFile()
    player = configs.get('player')

    return player


def arguments():
    args = argParser()

    normal = 'https://www.twitch.tv/'
    mobile = 'https://m.twitch.tv/'

    vod_normal = normal + 'videos/'
    vod_mobile = mobile + 'videos/'

    def checkLinkMobile():
        streamerretriever = initStreamerRetriever()
        online = streamerretriever.getOnline()
        if args.check:
            for o in online:
                print(o.getDispName())
        elif args.mobile:
            for o in online:
                print(mobile + o.getName())
        else:
            for o in online:
                print(normal + o.getName())

    def playWeb():
        streamerretriever = initStreamerRetriever()

        online = streamerretriever.getOnline()
        if not online:
            return
        value = askInput(online, showDispName)
        if not value:
            return

        if args.mobile and args.web:
            url = mobile + value.getName()
            logger.info(f'Twitch URL: {url}')
            webbrowser.open(url)
        elif args.web:
            url = normal + value.getName()
            logger.info(f'Mobile URL: {url}')
            webbrowser.open(url)
        elif args.mobile:
            url = mobile + value.getName()
            command = getPlayer()
            command.append(url)
            logger.info(f'Mobile Command: {command}')
            subprocess.Popen(command, close_fds=True)
        else:
            url = normal + value.getName()
            command = getPlayer()
            command.append(url)
            logger.info(f'Twitch Command: {command}')
            subprocess.Popen(command, close_fds=True)

    def playVod():
        streamerretriever = initStreamerRetriever()

        database = streamerretriever.getDb()
        if not database:
            return
        value = askInput(database, showDispName)
        if not value:
            return

        vodPrinting(value)

        vods = streamerretriever.getVod(value.getUserId())
        if not vods:
            return
        chosen_vod = askInput(vods, showVodInfo)
        if not chosen_vod:
            return

        if args.mobile and args.web:
            url = vod_mobile + chosen_vod.getVodId()
            logger.info(f'Vod URL: {url}')
            webbrowser.open(url)
        elif args.web:
            url = vod_normal + chosen_vod.getVodId()
            logger.info(f'Vod URL: {url}')
            webbrowser.open(url)
        elif args.mobile:
            url = vod_mobile + chosen_vod.getVodId()
            command = getPlayer()
            command.append(url)
            logger.info(f'Vod Mobile: {url}')
            subprocess.Popen(command, close_fds=True)
        else:
            url = vod_normal + chosen_vod.getVodId()
            command = getPlayer()
            command.append(url)
            logger.info(f'Vod Command: {command}')
            subprocess.Popen(command, close_fds=True)

    if args.version:
        print(f'{constants.__version__}')
    elif args.vod:
        playVod()
    elif args.play or args.web:
        playWeb()
    elif args.check or args.link or args.mobile:
        checkLinkMobile()
    elif args.twitch_follows:
        streamerretriever = initStreamerRetriever()
        # print(streamerretriever.getValidate().getId())
        for f in streamerretriever.getTwitchFollows():
            print(f.getName())


def main():
    try:
        arguments()
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
