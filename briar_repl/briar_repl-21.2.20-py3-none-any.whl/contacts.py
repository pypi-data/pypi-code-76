import datetime
from pprint import pprint
import colorful as col
from .start_up import URLS
from .repl import prompt_session as ps
from .repl import msgs_completer, com_completer
from .network import req_get, req_post, req_put, req_delete
from dataclasses import dataclass


@dataclass
class Contact:
    cid           : int  = 0
    name          : str  = ""
    alias         : str  = ""
    is_online     : bool = False
    unread_msgs   : int  = 0
    unread_count  : int  = 0
    pub_key       : str  = ""
    verified      : bool = False
    last_activity : int  = 0


async def init_contacts():
    global online
    json_resp = await req_get(
        URLS.contacts,
        topic="get_contacts",
    )
    for c in json_resp:
        alias_or_name = c.get("alias") or c["author"]["name"]
        contact = Contact(
            cid=c["contactId"],
            name=c["author"]["name"],
            alias=alias_or_name,
            is_online=c["connected"],
            # unread_msgs=c["unreadCount"],
            unread_count=c["unreadCount"],
            verified=c["verified"],
            pub_key=c["author"]["publicKey"],
            last_activity=c["lastChatActivity"]
        )
        all_contacts[c["contactId"]] = contact
        all_contacts_by_alias[alias_or_name] = contact
        if contact.is_online:
            online += 1
    msgs_completer.extend(all_contacts_by_alias.keys())
    msgs_completer.sort()
    com_completer.extend(all_contacts_by_alias.keys())
    com_completer.sort()


async def show_contacts(detailed=None):
    """
    lists your contacts
    """
    print(f"  > your {len(all_contacts)} contacts:")
    contacts_by_last_act = sorted(
        list(all_contacts.values()),
        key=lambda k: k.last_activity,
        reverse=True
    )
    for contact in contacts_by_last_act:
        contact_online = col.bold_chartreuse("online") if contact.is_online else ""
        unread_count = contact.unread_msgs if contact.unread_msgs else ''
        last_act = datetime.datetime.fromtimestamp(contact.last_activity / 1000).strftime('%Y-%m-%d %H:%M')
        if detailed:
            verified = col.bold_chartreuse("V") if contact.verified else col.bold_coral("X")
            print(f"{contact.cid:4} {verified} {last_act} {contact.unread_msgs:2} {contact.unread_count:2}: "
                  f"{contact.alias} {contact_online} {col.bold_orange(unread_count)}")
        else:
            print(f"    {contact.alias} {contact_online} {col.bold_orange(unread_count)}")


async def show_contacts_detailed():
    """
    lists your contacts with details
    """
    await show_contacts(detailed=True)


async def show_contact_info(contact_str=None):
    """
    shows contact info
    """
    if not contact_str:
        print("not contact was specified")
        contact_str = await ps.prompt_async("please specify contact:")
        # print(f"now got: {contact_str}")
    contact = await get_contact_id_by_alias(contact_str)
    if not contact:
        print(f"contact {contact_str} not found")
        return
    pprint(contact.__dict__)


async def show_raw_contacts_info():
    """
    shows raw contacts info
    """
    json_resp = await req_get(
        URLS.contacts,
        topic="get_contacts",
    )
    for c in json_resp:
        pprint(c)


async def get_contact_id_by_alias(alias):
    if all_contacts_by_alias.get(alias):
        return all_contacts_by_alias[alias]


async def get_pending_contacts():
    json_resp = await req_get(
        URLS.contacts_pending,
        topic="get_pending_contacts",
    )
    return json_resp


async def show_pending_contacts():
    """
    lists pending contacts
    """
    pending_contacts = await get_pending_contacts()
    if not pending_contacts:
        print("  > no pending_contacts")
        return
    print(f"  > your {len(pending_contacts)} pending contacts:")
    for contact in pending_contacts:
        #print(f"{contact['contactId']:4}: {contact['alias']}")
        pprint(contact)


async def remove_pending_contact(contact_str):
    """
    removes pending contact
    """
    print(f"want to remove pending contact: {contact_str}")
    pending_contacts = await get_pending_contacts()
    pending_contacts_by_alias = {con["pendingContact"]["alias"]:con["pendingContact"]["pendingContactId"]
                                 for con in pending_contacts}
    if not pending_contacts_by_alias.get(contact_str):
        print(f"sorry did not find {contact_str} in pending contacts")
        return
    contact_id = pending_contacts_by_alias.get(contact_str)
    print(f"would remove found pending contact: {contact_str} - {contact_id}")
    remove_contact = {
        "pendingContactId": contact_id,
    }
    pprint(remove_contact)
    json_resp = await req_delete(
        URLS.contacts_pending,
        topic="get_pending_contacts",
        params=remove_contact,
    )
    return json_resp


async def add_contact(briar_link, alias):
    """
    add contact with briar_link and alias
    """
    add_contact = {
        "link": briar_link,
        "alias": alias,
    }
    json_resp = await req_post(
        url=URLS.contacts_pending,
        json_data=add_contact,
        topic=f"add_contact {alias} - {briar_link}",
    )
    return json_resp


async def rename_contact(contact_str, new_alias):
    """
    renames a contact with new alias
    """
    contact = await get_contact_id_by_alias(contact_str)
    if not contact:
        print(f"contact {contact_str} not found")
        return
    json_resp = await req_put(
        url=f"{URLS.contacts}/{contact.cid}/alias",
        json_data={"alias": new_alias},
        topic=f"renames_contact {contact_str} to {new_alias}",
    )
    await init_contacts()
    await show_contacts()
    return json_resp


async def remove_contact(contact_str):
    """
    removes a contact
    """
    contact = await get_contact_id_by_alias(contact_str)
    if not contact:
        print(f"contact {contact_str} not found")
        return
    json_resp = await req_delete(
        url=f"{URLS.contacts}/{contact.cid}",
        topic=f"remove_contact {contact.cid}",
    )
    if json_resp:
        print(f"contact: {contact.alias} {contact.cid} - successfully deleted.")
    return json_resp


async def get_own_briar_link():
    json_resp = await req_get(
        url=URLS.link,
        topic="get_own_briar_link",
    )
    return json_resp


async def show_own_briar_link():
    """
    displays your own briar link
    """
    link = await get_own_briar_link()
    print(f"  > your own briar link: \n    {link['link']}")


all_contacts          = {}
all_contacts_by_alias = {}
current_contact = {"id": 0, "alias":""}
online = 0
