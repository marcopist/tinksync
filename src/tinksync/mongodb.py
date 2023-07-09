from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
mongoClient = MongoClient(MONGO_CONNECTION_STRING, server_api=ServerApi('1'))
usersCollection = mongoClient['tinksync']['users']

def get_user_settings(username):
    document = usersCollection.find_one({"username": username})
    return document

def replace_user_settings(record):
    id_ = record['_id']
    usersCollection.replace_one({"_id": id_}, record)

def insert_user_settings(record):
    usersCollection.insert_one(record)