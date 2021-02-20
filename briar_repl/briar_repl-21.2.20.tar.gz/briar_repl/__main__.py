"""briar cli-messenger for briar:headless"""

import asyncio
import types
from . import connections as conn
from . import contacts as cont
from . import messages as msgs
from . import repl
from .repl import prompt_session as ps
from .repl import help, exit_repl, quit_repl, version_info
from .contacts import init_contacts, show_contacts, \
    show_pending_contacts, remove_pending_contact, \
    add_contact, remove_contact, show_own_briar_link, \
    show_contact_info, show_raw_contacts_info, \
    show_contacts_detailed, rename_contact
from .blogs import show_blog_posts, post_blog_entry


# TODO add dialog to kwargs functions when kwargs not supplied


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(conn.probe_headless())
    loop.create_task(conn.connect_websocket())
    loop.run_until_complete(init_contacts())
    loop.run_until_complete(show_contacts())
    loop.run_until_complete(chose_action())
    loop.close()


async def chat_raw_msgs_with(contact_str):
    """
    debug view: chats with specific contact in 1:1 chat
    """
    await chat_with(contact_str, limit=-7, raw_msgs=True)


async def chat_full_history_with(contact_str):
    """
    chats with specific contact in 1:1 chat full history
    """
    await chat_with(contact_str, limit="all")


async def chat_with(contact_str, limit=None, raw_msgs=None):
    """
    chats with specific contact in 1:1 chat
    """
    if cont.all_contacts_by_alias.get(contact_str):
        contact = await cont.get_contact_id_by_alias(contact_str)
        contact_id = contact.cid
    else:
        print(f"contact {contact_str} not found..")
        return
    with repl.patch_stdout():
        cont.current_contact["id"] = contact_id
        cont.current_contact["alias"] = contact_str
        await msgs.show_history(
            contact_id,
            limit_last=limit,
            raw_msgs=raw_msgs
        )
        msgs.unread -= cont.all_contacts[contact_id].unread_msgs
        cont.all_contacts[contact_id].unread_msgs = 0
        cont.all_contacts[contact_id].unread_count = 0
        await send_msgs(contact_id)
        cont.current_contact["id"] = 0
        cont.current_contact["alias"] = ""
        print("leaving chat..")


async def send_msgs(contact_id):
    repl.mode = "send_msgs"
    while True:
        msg_text = await ps.prompt_async(
            "msg: ",
            style=repl.prompt_style_chat,
            completer=repl.repl_completer(repl.msgs_completer),
        )
        if msg_text == "/back":
            break
        if msg_text == "/exit_chat":
            break
        elif msg_text.startswith("/"):
            command, *args = msg_text[1:].split()
            if command in repl.implemented:
                # print(f"this now runs command: {command} with args: {args}")
                perform = repl.implemented.get(command)
                await perform(*args)

            else:
                print("sorry could not find this command..")

        elif len(msg_text) > 0:
            await msgs.send(contact_id, msg_text)


async def chose_action():
    repl.mode = "chose_action"
    while True:
        action = await ps.prompt_async(
            "com: ", 
            completer=repl.com_completer,
            style=repl.prompt_style_commands,
        )
        if not action:
            continue
        command, *args = action.split()
        if command in repl.implemented:
            # print(f"this now runs command: {command} with args: {args}")
            perform = repl.implemented.get(command)
            await perform(*args)
        else:
            print("sorry could not find this command..")


if __name__ == "__main__":
    repl.implemented = {
        key: val for key, val in globals().items()
        if isinstance(val, types.FunctionType)
           and key not in repl.hidden
    }
    repl.com_completer.extend(repl.implemented)
    repl.com_completer.sort()
    repl.com_completer = repl.repl_completer(repl.com_completer)
    contact_info = {}
    # print(repl.implemented.keys())
    main()
