# -*- coding: utf-8 -*-

import pymongo

RESOURCES = {}
CONF = {}

ALL = [
    "initMongo",
    "getMongoClient"
]


class MongoExcept(Exception):
    pass


def new_mongo(**kwargs):
    mongdb_client = pymongo.MongoClient(kwargs.get("uri"))
    admin_db = mongdb_client[kwargs.get("auth")]
    admin_db.authenticate(kwargs.get("user"),kwargs.get("password"))
    return mongdb_client

def initMongo(**kwargs):
    CONF["conf"] = kwargs
    mongdb_client = new_mongo(**kwargs)
    name = kwargs.get("name")
    if not name:
        name = "base"
    RESOURCES[name] = mongdb_client

def getMongoClient(name="base"):
    client = RESOURCES.get(name)
    if not client:
        kwargs = CONF.get("conf")
        if not kwargs:
            raise MongoExcept("mongo模块未初始化")
        mongdb_client = new_mongo(**kwargs)
        RESOURCES[name] = mongdb_client
        return mongdb_client
    return client

        
        