import sqlite3

import pymongo

from config import mongo_access

# set connection with sqlite db
def connect_db():
    return sqlite3.connect(r"./db/f1db.db")


# configure mongodb client
def mongo_config():
    client = pymongo.MongoClient(mongo_access)
    db = client.f1db
    return db


# helper for repeatable inserting
def mongo_upsert(data, collection):
    data = dict(data)
    collection.update_one({"_id": data["_id"]}, {"$set": data}, upsert=True)
