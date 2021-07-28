from loguru import logger
from app.core.mongo import get_database
from data.data import templates_1, templates_2

dbname = get_database()
collection_name = dbname["templates"]
try:
    item_details = collection_name.delete_many({})
except Exception as err:
    logger.debug(f"ERR: {err}")

try:
    result = collection_name.insert_many([*templates_1, *templates_2])
except Exception as err:
    logger.debug(f"ERR: {err}")
