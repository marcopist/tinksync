from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
mongoClient = MongoClient(MONGO_CONNECTION_STRING, server_api=ServerApi('1'))
mongoCollection = mongoClient['tinksync']['users']

def get_user(username):
    document = next(mongoCollection.find({"username": username}))
    id = document['_id']
    content = {k: v for k, v in document.items() if k != '_id'}
    return id, content

def replace_record(id, record):
    mongoCollection.replace_one({"_id": id}, record)
