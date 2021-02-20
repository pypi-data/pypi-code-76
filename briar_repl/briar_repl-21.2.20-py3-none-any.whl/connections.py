import asyncio
import json
import websockets
import colorful as col
from .start_up import URLS, TOKEN, HOST, PORT
from.network import probe_req_get
from . import messages as msgs
from . import contacts as cont


async def probe_headless():
    json_resp = await probe_req_get(
        url=URLS.link,
        topic="probe if briar-headless can be connected to"
    )
    if json_resp.get("error"):
        print(col.bold_coral(
            f"ERROR: {json_resp} could not connect to briar-headless! \n"
            f"expected at: {HOST}:{PORT}"
        ))
        quit(2)
    if json_resp:
        print(col.bold_chartreuse(
            "connection to headless successful!\n"
        ))


async def connect_websocket():
    async with websockets.connect(URLS.ws) as ws:
        await ws.send(TOKEN)
        await get_message_websocket(ws)


async def get_message_websocket(ws):
    # print(f"get_message_websocket CHAT_WITH: {cont.current_contact['id']}")
    while not ws.closed and not asyncio.get_event_loop().is_closed():
        message = await ws.recv()
        msg = json.loads(message)
        if msg['name'] == 'ConversationMessageReceivedEvent':
            if not msg['data']['contactId'] == cont.current_contact['id']:
                # print(f"message from someone else: {msg['data']['contactId']} , not: {cont.current_contact['id']}")
                cont.all_contacts[msg['data']['contactId']].unread_msgs += 1
                msgs.unread += 1
                continue
            print()  # line-break
            await msgs.print_message(msg['data'])
            print("", end='', flush=True)
        elif msg['name'] == 'ContactConnectedEvent':
            # print(msg)
            cont.all_contacts[msg['data']['contactId']].is_online = True
            cont.online += 1
            # {'type': 'event', 'name': 'ContactDisconnectedEvent', 'data': {'contactId': 4}}
        elif msg['name'] == 'ContactDisconnectedEvent':
            # print(msg)
            cont.all_contacts[msg['data']['contactId']].is_online = False
            cont.online -= 1
            # {'type': 'event', 'name': 'ContactDisconnectedEvent', 'data': {'contactId': 4}}
    if not asyncio.get_event_loop().is_closed():
        asyncio.get_event_loop().create_task(get_message_websocket(ws))

