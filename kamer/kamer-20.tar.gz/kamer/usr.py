# OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide
#
# This file is placed in the Public Domain.

"users"

# imports

import logging

from op.dbs import find
from op.obj import Object, get, save

# classes

class ENOUSER(Exception):

    pass

class User(Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Object):

    userhosts = Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = get(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return find("kamer.usr.User", s)

    def get_user(self, origin):
        u = list(self.get_users(origin))
        logging.error(u)
        if u:
            return u[-1][-1]

    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user

# commands

def dlt(event):
    if not event.args:
        return
    selector = {"user": event.args[0]}
    for fn, o in find("kamer.usr.User", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def met(event):
    if not event.args:
        return
    user = User()
    user.user = event.rest
    user.perms = ["USER"]
    save(user)
    event.reply("ok")
