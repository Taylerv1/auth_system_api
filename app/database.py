from pymongo import MongoClient

from app.config import settings


client = MongoClient(settings.mongo_uri)
database = client[settings.database_name]
users_collection = database["users"]


def create_indexes():
    users_collection.create_index("email", unique=True)
