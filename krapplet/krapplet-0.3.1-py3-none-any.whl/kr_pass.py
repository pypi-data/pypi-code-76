#!/usr/bin/env python3

"""
kr_pass: the krapplet pass storage provider
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import os
import sys
import time
from typing import Dict, Iterator, Optional
from subprocess import check_output, PIPE, STDOUT


# python-gnupg is a Python wrapper for gpg
try:
    import gnupg
except:
    sys.stderr.write("Please install python-gnupg")
    sys.exit(1)


# Assume gtk availability check done in krapplet.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk


HOME_DIR = os.path.expanduser("~")
DEFAULT_PASSWORD_STORE = HOME_DIR + "/.password-store"
GPG_ID_FILE = DEFAULT_PASSWORD_STORE + "/.gpg-id"
PASSWORD_STORE = DEFAULT_PASSWORD_STORE
VERBOSE = False
ARMOR = False                         # default no ASCII encoding of secrets
DIR_PERMISSIONS = 0o700               # read/write/execute  user only
FILE_PERMISSIONS = 0o600              # read/write user only
DEFAULT_COLLECTION = "????"
GPG_ID = ""


# Exception classes:
class PassException(Exception):
    """All exceptions derive from this class."""
    pass

class NotAvailableException(PassException):
    pass

class LockedException(PassException):
    pass

class KeyNotFoundException(PassException):
    pass

class PromptDismissedException(PassException):
    pass


def gpg_id():
    """ retrieves the gpg-id from file ${HOME}/.password-store/.gpg-id """
    rval = ""
    try: 
        with open(GPG_ID_FILE) as fh:
            rval = fh.read()
    except:
        print("Gpg_id not found")
    return rval


def encrypt(unenc: str, recipients: str, passphrase: str) -> str:
    """ Encrypts a string using the passphrase """
    gpg = gnupg.GPG(verbose=VERBOSE, use_agent=False)
    enc = gpg.encrypt(unenc, passphrase=passphrase, sign=True,
                      recipients = recipients, armor = ARMOR)
    if enc.ok:
        return enc.data
    else:
        return ""


def passwd_test( recipients: str, passphrase: str) -> bool:
    """ tests if we can encrypt a string """
    enc = encrypt("An unecrypted string", recipients, passphrase)
    return len( enc ) > 0


class Connection():
    """ This class maintains the passhrase for gpg """

    passphrase = ""                             # class var over all instances
    recipients = gpg_id().strip()

    def check_validty(self) -> None:
        """ Clears the password when encryption of a string fails """
        return
        if not passwd_test(Connection.recipients, Connection.passphrase):
            self.lock()

    def get_passphrase(self) -> str:
        """ performs validity check and returns the password str,
            or "" when it was cleared """
        self.check_validty()
        return Connection.passphrase

    def set_passphrase(self, passphrase: str) -> None:
        """ set the passphrase for the connection,
        in fact unlocking the connection """
        if passwd_test(Connection.recipients, Connection.passphrase):
            Connection.passphrase = passphrase

    def lock(self) -> None:
        """ Locks a connection by clearing the passphrase """
        Connection.passphrase = ""
        msg = check_output(["gpgconf", "--reload", "gpg-agent"],
                           stderr=STDOUT ).decode("utf-8")

    def is_locked(self) -> bool:
        """ Returns the current lock state of a connection """
        self.check_validty()
        is_locked = Connection.passphrase == ""
        return is_locked

    def close(self) -> None:
        # ignore, keep class vars for next instance
        pass


def connection_open() -> Connection:
    """ Opens the connection to the pass store, verifies it existence """
    conn = Connection()
    return conn


def set_armor(val: bool) -> None:
    """ Sets the global variabe ARMOR """
    global ARMOR
    ARMOR = val


def check_gpg( gpg_id ) -> None:
    """ rudimentary check for a gpg_id, exits when gpg
    command or gpg-id not found """
    return


class PasswordEntryDialog(Gtk.Dialog):
    """ PasswordEntryDialog: pops up a window to ask for a password """
    def __init__(self, parent, title: str, unlock_item: str) -> None:
        Gtk.Dialog.__init__(self, title=title, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        box = self.get_content_area()
        password_prompt = Gtk.Label(label=unlock_item, xalign=0)
        self.passord_entry = Gtk.Entry(xalign = 0, visibility=False)
        self.passord_entry.set_activates_default(True)
        self.set_default_response(Gtk.ResponseType.OK)
        grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        box.add(grid)
        grid.attach_next_to(password_prompt, None,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.passord_entry, password_prompt, 
                            Gtk.PositionType.RIGHT, 1, 1)
        self.show_all()

    def get_pw( self ) -> str:
        return self.passord_entry.get_text()


class Key(object):
    """Represents a secret item."""
    def __init__(self, connection, path: str, session = None) -> None:
        self.path = path
        self.session = session
        self.connection = connection
        self.attrs = {}
        self.secret = ""
        self.recipients = gpg_id().strip()
        self.created = self.modified = 0

    def __eq__(self, other) -> bool:
        assert isinstance(other.path, str)
        return self.path == other.path

    def save_encrypted(self) -> None:
        """ saves key data encrypted"""
        unenc_str = self.secret + "\n"
        for name in self.attrs.keys():
            unenc_str += name + ": " + self.attrs[name] + "\n"
        enc = encrypt(unenc_str, self.connection.recipients,
                      self.connection.get_passphrase())
        if len(enc): 
            with open(os.open(self.path,
                              os.O_CREAT | os.O_WRONLY, FILE_PERMISSIONS),
                      "wb") as fh:
                fh.write( enc )

    def read_encrypted(self) -> bool:
        gpg = gnupg.GPG(verbose=VERBOSE, use_agent=False)
        passphrase=self.connection.get_passphrase()
        with open(self.path, 'rb') as f:
            dec = gpg.decrypt_file(f, passphrase=passphrase)
        if dec.ok:
            _, fname = os.path.split(self.path)
            label, _ = os.path.splitext(fname)
            self.created = self.modified = 0
            lines = str(dec).splitlines()
            secret = ""
            for line in lines:
                if not len(secret):            # first line contains the secret
                    secret = line
                    self.secret = secret
                else:                          # next lines contain the attribs
                    colon_idx = line.find(':')
                    name = line[:colon_idx]
                    val = line[colon_idx+2:]
                    self.attrs[name] = val
            return True
        else:
            print("Could not read decrypted file, status:", dec.status)
        return False

    def is_locked(self) -> bool:
        """Returns :const:`True` if item is locked, otherwise :const:`False`."""
        return self.connection.is_locked()

    def ensure_not_locked(self) -> None:
        """If kehyring is locked, raises: LockedException"""
        if self.connection.is_locked():
            self.unlock()
            #raise LockedException("Item is locked!')

    def lock(self) -> None:
        """ Lock the connection """
        self.connection.lock()

    def unlock(self) -> bool:
        """ to simulate unlocking, a password prompt is showm,
            the password is captured, and with the password we try to decrypt
            the key. Return True if successful, False otherwise """
        while self.is_locked():
            dialog = PasswordEntryDialog(self, title = "Unlock",
                                         unlock_item = "Passphrase")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.connection.set_passphrase(dialog.get_pw())
                if self.read_encrypted():
                    dialog.destroy()
                    return True
                else:
                    self.lock()
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                return False
            dialog.destroy()

    def get_attributes(self) -> Dict[str, str]:
        """Returns item attributes (dictionary)."""
        if self.attrs == {}:
            self.read_encrypted()
        return self.attrs

    def set_attributes(self, attributes: Dict[str, str]) -> None:
        """ Sets item attributes to attributes """
        self.ensure_not_locked()
        self.attrs = attributes
        self.save_encrypted() 

    def get_label(self) -> str:
        _, fname = os.path.split(self.path)
        label, _ = os.path.splitext(fname )
        return label

    def set_label(self, label: str) -> None:
        """ the label is the last part of the itempath, 
        changing the label means renamiing the file """
        self.ensure_not_locked()
        dname, fname = os.path.split(self.path)
        base, ext = os.path.splitext(fname)
        new_fname = label + ext
        newpath = os.path.join(dname, new_fname)
        if not self.path == newpath:
            os.rename(self.path, newpath)
            self.path = newpath

    def delete(self) -> None:
        """ just delete the file? """
        os.remove(self.path)
        self.attrs = {}
        self.secret = ""

    def get_secret(self) -> bytes:
        """Returns item secret (bytestring)."""
        if len( self.secret ) == 0:
            self.read_encrypted()
        return str.encode(self.secret)

    def get_secret_content_type(self) -> str:
        """ Not supported as such, therefore always return text/plain """
        return "text/plain"

    def set_secret(self, secret: bytes, 
                   content_type: str = 'text/plain') -> None:
        """Sets secret to `secret`,
           content_type is there for compat reasons, but is ignored """
        self.ensure_not_locked()
        self.secret = secret.decode("utf-8")
        self.save_encrypted()

    def get_created(self) -> int:
        """Returns UNIX timestamp (integer), when the item was created. """
        statinfo = os.stat(self.path)
        return statinfo.st_ctime

    def get_modified(self) -> int:
        """Returns UNIX timestamp (integer), when the item was last modified."""
        statinfo = os.stat(self.path)
        return statinfo.st_mtime

    def move(self, new_keyring_label):
        """ moves a key to a different keyring """
        keyrings = get_all_keyrings(self.connection)
        for keyring in keyrings:
            if keyring.get_label() == new_keyring_label:
                _, fname = os.path.split(self.path)
                newpath = os.path.join(keyring.path, fname)
                os.replace(self.path, newpath)
                self.path = newpath
                return


class Keyring(object):
    """Represents a kehyring."""

    def __init__(self,
                 connection: Connection, 
                 path: str = DEFAULT_COLLECTION,
                 session = None) -> None:
        self.connection = connection
        self.session = session
        self.path = path

    def is_locked(self) -> bool:
        """Returns :const:`True` if item is locked, otherwise :const:`False`."""
        is_locked = self.connection.is_locked()
        return is_locked

    def ensure_not_locked(self) -> None:
        """If keyring is locked, raises LockedException"""
        if self.is_locked():
            raise LockedException('Keyring is locked!')

    def unlock(self) -> bool:
        """ Attempts to unlock a Keyring, currently not using the gpg-agent """
        is_locked = self.is_locked()
        while is_locked:
            dialog = PasswordEntryDialog(self, title="Unlock",
                                         unlock_item =  "Passphrase")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                passwd = dialog.get_pw()
                if passwd_test(self.connection.recipients, passwd):
                    self.connection.set_passphrase(passwd)
                is_locked = self.is_locked()
            dialog.destroy()
            if response == Gtk.ResponseType.CANCEL:
                break
        return self.is_locked()

    def lock(self) -> None:
        """Locks the keyring."""
        self.connection.lock()

    def delete(self) -> None:
        """Deletes the keyringi and all keys attached to it."""
        self.ensure_not_locked()
        for dirname, dirs, files in os.walk(self.path, topdown = False):
            for d in dirs:
                os.rmdir(os.path.join(dirname, d))
            for f in files:
                os.remove(os.path.join(dirname, f))
        os.rmdir(self.path)
        self.path = None

    def get_all_keys(self) -> Iterator[Key]:
        """Returns a generator of all keys on the keyring."""
        for fname in os.listdir(self.path):
            keypath = os.path.join(self.path, fname)
            if os.path.isfile(keypath) and keypath.endswith(".gpg"):
                yield Key(self.connection, keypath, None)

    def search_items(self, attributes: Dict[str, str]) -> Iterator[Key]:
        """Returns a generator of keys with the given attributes."""
        if not self.is_locked():
            for key in self.get_all_keys():
                key_attributes = key.get_attributes()
                for attrib in key_attributes:
                    if attrib == attributes:
                        return key
        else:
            return
            yield 

    def get_label(self) -> str:
        """Returns the keyring label."""
        _, label = os.path.split( self.path )
        return label 

    def set_label(self, label: str) -> None:
        """ the label is the last part of the keyring path,
            changing the label means renamiing the dir """
        self.ensure_not_locked()
        path, oldlabel = os.path.split(self.path)
        newpath = os.path.join(path, label)
        if not self.path == newpath:
            os.rename(self.path, newpath)
            self.path = newpath


    def create_key(self, label: str, attributes: Dict[str, str],
                   secret: bytes, replace: bool = False,
                   content_type: str = 'text/plain') -> Key:

        """ Creates a key and returns it """
        self.ensure_not_locked()
        path = os.path.join(self.path, label + ".gpg")
        if replace or not os.path.isfile(path):
            key = Key(self.connection, path)
            key.set_secret(secret)
            key.set_attributes(attributes)
            return key
        return None                     # FIXME: raise an exception ?



def create_keyring(connection: Connection, label: str, 
                   alias: str = '', session = None) -> Keyring:
    """Creates a new keyring and returns it. Alias and session are ignored
    for this implementation it only requires a directory to be created """

    path =  os.path.join(DEFAULT_PASSWORD_STORE, label)
    if not os.path.exists(path):
        os.mkdir(path)
    if os.path.isdir(path):
        os.chmod(path, DIR_PERMISSIONS)
        return Keyring(connection, path)
    else:
        return None


def get_all_keyrings(connection) -> Iterator[Keyring]:
    """Returns a generator of all available keyrings."""
    for dname in os.listdir(DEFAULT_PASSWORD_STORE):
        path = os.path.join(DEFAULT_PASSWORD_STORE, dname)
        if os.path.isdir(path):
            yield Keyring(connection, path)


def get_default_keyring(connection,session = None) -> Keyring:
    """Returns the default keyring. If it doesn't exist, creates it."""
    defaultpath = os.path.join(DEFAULT_PASSWORD_STORE, "default")
    if os.path.isdir(defaultpath):
        return Keyring(connection, defaultpath)
    else:
        return Keyring( connection, "default" )

def get_any_keyring(connection) -> Keyring:
    """Returns any keyring, in the following order of preference:
    - The default keyring;
    - The "session" keyring (usually temporary);
    - The first keyring in the keyring list."""

    defaultpath = os.path.join(DEFAULT_PASSWORD_STORE, "default")
    if os.path.isdir(defaultpath):
        return Keyring(connection, defaultpath)
    else:
        for entry in os.listdir(DEFAULT_PASSWORD_STORE):
            path = path.join(DEFAULT_PASSWORD_STORE, entry)
            if os.path.isdir(path):
                return Keyring(connection, path)
    raise KeyNotFoundException('No keyring found.')


def get_keyring_by_alias(connection, alias: str) -> Keyring:
    """Returns the keyring with the given `alias`. If there is no
    such keyring, raises KeyNotFoundException"""

    path = os.path.join(DEFAULT_PASSWORD_STORE, alias)
    if os.path.isdir(path):
        return Keyring(connection, path)
    raise KeyNotFoundException('No keyring found.')


def search_keys(connection, attributes: Dict[str, str]) -> Iterator[Key]:
    """Returns a generator of keys in all keyrings with the given
    attributes. `attributes` should be a dictionary."""
    for entry in os.listdir(DEFAULT_PASSWORD_STORE):
        path = os.path.join(DEFAULT_PASSWORD_STORE, entry)
        if os.path.isdir(path):
            keyring = Keyring(connection, path)
            return keyring.search_items(attributes)

