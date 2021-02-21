#!/usr/bin/env python3

"""
kr_secretservice: the krapplet secretservice backend
This is just a wrapper around secretstorage, other backends should
implement the same API as secretstorage provides
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applie
"""

import sys

try:
    import secretstorage
except:
    sys.stderr.write("Please install the secretstorage package")
    sys.exit( 2 )


# name redefinitions only: collections are keyrings, and items are keys

Key = secretstorage.Item
Keyring = secretstorage.Collection

connection_open  = secretstorage.dbus_init
create_keyring   = secretstorage.create_collection
search_keys      = secretstorage.search_items
get_all_keyrings = secretstorage.get_all_collections
Keyring.get_all_keys = Keyring.get_all_items
Keyring.create_key   = Keyring.create_item

NotAvailableException = secretstorage.SecretServiceNotAvailableException
LockedException       = secretstorage.LockedException
KeyNotFoundException  = secretstorage.ItemNotFoundException
PromptDismissedException = secretstorage.PromptDismissedException

def movekey(key, new_keyring_label):
    """ Add on function to move keys from one keyring to another one """

    keyrings = get_all_keyrings(key.connection)
    for keyring in keyrings:
        if keyring.get_label() == new_keyring_label:
            label   = key.get_label()
            attribs = key.get_attributes()
            secret  = key.get_secret()
            key.delete()
            key = keyring.create_key(label, attribs, secret)
            return key

Key.move = movekey

