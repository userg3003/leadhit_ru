import json

from bson import json_util
from pymongo import MongoClient

from app.core.config import settings


def get_database() -> MongoClient:
    """Получить коллекцию из базы MongoDb"""
    connection_string = settings.MONGO_URI
    client = MongoClient(connection_string)
    return client[settings.COLLECTION]


def get_templates(dbname: MongoClient, set_of_fields: set) -> list:
    """ Получить список шаблонов в которых присутствует хотя бы одно из полей заданных в set_of_fields """
    collection_name = dbname["templates"]
    item_fields = [{item[0]: {"$exists": True}} for item in set_of_fields]
    item_details = collection_name.find({"$or": item_fields})

    all_data = []
    for item in item_details:
        all_data.append(item)
    return all_data


def all_templates(dbname: MongoClient) -> list:
    """Получить список всех шаблонов из базы."""
    collection_name = dbname["templates"]
    item_details = collection_name.find()
    all_data = []
    for item in item_details:
        all_data.append(json.loads(json_util.dumps(item)))
    return all_data
