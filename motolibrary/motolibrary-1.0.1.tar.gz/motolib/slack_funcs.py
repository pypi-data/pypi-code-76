# slack_funcs.py

from slack import WebClient
from slack.errors import SlackApiError
import sys


def slack_send_message(slackbot_token, channels, messages):
    """
    -------------------------------------------------------
    Sends slack message(s) to specified channel(s)
    Use: slack_send_message(channels, messages))
    -------------------------------------------------------
    Parameters:
        slackbot_token: string
            token for slack bot usage
        channels: list
            contains list of channels to send messages to via slack
        messages: list
            contains list of messages to send
    Returns:
       NONE
    ------------------------------------------------------
    """
    sys.dont_write_bytecode = True

    client = WebClient(token=slackbot_token)

    for channel in channels:
        for message in messages:
            response = client.chat_postMessage(channel=channel, text=message)
    return


def slack_send_file(slackbot_token, channels, files, titles):
    """
    -------------------------------------------------------
    Sends file(s) to specified channel(s)
    Use: slack_send_file(channels, files, titles)
    -------------------------------------------------------
    Parameters:
        slackbot_token: string
            token for slack bot usage
        channels: list
            contains list of channels to send messages to via slack
        files: list
            contains list of files to send
        titles: list
            contains list of titles of files; titles shoud correspond to same
            order of items in files list.
    Returns:
       NONE
    ------------------------------------------------------
    """
    client = WebClient(token=slackbot_token)

    for channel in channels:
        i = 0
        for file in files:
            title = titles[i]
            client.files_upload(channels=channel, file=file, title=title)
            i += 1
    return
