from pprint import pprint
import datetime
import colorful as col
from . import contacts as cont
from .start_up import URLS
from .network import req_get, req_post

# TODO remove doubled own messages


async def send(contact_id, text):
    json_resp = await req_post(
        url=URLS.msgs + str(contact_id),
        json_data={'text': text},
        topic=f"send_message to {contact_id}"
    )
    await print_message(json_resp)


async def get_history(contact_id):
    json_resp = await req_get(
        url=URLS.msgs + str(contact_id),
        topic="get_history"
    )
    # pprint(json_resp) # messgaes debug
    return json_resp


async def show_history(contact_id, limit_last=None, raw_msgs=None):
    limit_last = limit_last or -15
    history = await get_history(contact_id)
    if not history:
        print("no chat history found yet - starting here:")
        return
    if limit_last == -15:
        for message in history[limit_last:]:
            await print_message(message)
    elif raw_msgs:
        for message in history[limit_last:]:
            pprint(message)
            print()
    elif limit_last == "all":
        for message in history:
            await print_message(message)


async def print_message(message):
    correspondent = cont.current_contact["alias"] or ""
    prefix = 'me' if message['local'] else f'{correspondent}'
    time = await get_time(message['timestamp'])
    msgs_type = message["type"]
    if msgs_type == "PrivateMessage":
        if 'text' in message:
            # time_stamp = col.grey60(time)
            time_stamp = time
            print(f"{time_stamp} {prefix}:\n    {message['text']}\n")

        is_read = message['read']
        if not is_read:
            await mark_message_as_read(message)
    else:
        print(col.coral(f"unsupported message type: {msgs_type}\n"))


async def get_time(msg_time):
    # msg_time = datetime.datetime.fromtimestamp(msg_time / 1000).strftime('%Y-%m-%dT%H:%M:%S')
    msg_time = datetime.datetime.fromtimestamp(msg_time / 1000).strftime('%Y-%m-%d %H:%M')
    return msg_time


async def mark_message_as_read(message):
    msg_id = message["id"]
    msg_read = {"messageId": msg_id}
    resp = await req_post(
        url=URLS.msgs + str(message['contactId']) + "/read",
        json_data=msg_read,
        topic="mark_message_as_read",
    )
    # print(resp)


unread = 0
