from loguru import logger
from faker import Faker
from faker.providers import person, internet, python, date_time, address, company, job, lorem, misc, phone_number, \
    automotive
import pytest

from app.core.mongo import get_database


def make_fake():
    fake_ = Faker("ru_RU")
    fake_.add_provider(person)
    fake_.add_provider(internet)
    fake_.add_provider(python)
    fake_.add_provider(date_time)
    fake_.add_provider(address)
    fake_.add_provider(company)
    fake_.add_provider(job)
    fake_.add_provider(lorem)
    fake_.add_provider(misc)
    fake_.add_provider(phone_number)
    fake_.add_provider(automotive)
    return fake_


fake = make_fake()

templates_1 = [{
    "name": "FormOrder",
    "user_email": "email",
    "user_phone": "phone",
    "user_info": "text",
},
    {
        "name": "FormAnswer",
        "user_email": "email",
        "user_phone": "phone",
        "user_answer": "text",
    }]

templates_2 = [{
    "name": "FormFirmOrder",
    "сhief_email": "email",
    "сhief_phone": "phone",
    "firm_phone": "phone",
    "firm_email": "email",
    "user_phone": "phone",
},
    {
        "name": "FormFirmAnswer",
        "сhief_email": "email",
        "сhief_phone": "phone",
        "firm_phone": "phone",
        "firm_email": "email",
        "firm_info": "text",
    }]



@pytest.fixture(autouse=True)
def fill_db():
    """Connect to db before testing, disconnect after."""
    dbname = get_database()
    collection_name = dbname["templates"]
    try:
        collection_name.delete_many({})
    except Exception as err:
        logger.debug(f"ERR: {err}")

    try:
        collection_name.insert_many([*templates_1, *templates_2])
    except Exception as err:
        logger.debug(f"ERR: {err}")
    yield


    try:
        collection_name.delete_many({})
    except Exception as err:
        logger.debug(f"ERR: {err}")
