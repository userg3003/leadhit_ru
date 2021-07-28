from tests import fake, fill_db

from app.core.mongo import get_database


def test_fill_db(fill_db):
    dbname = get_database()
    collection_name = dbname["templates"]

    template1 = {
        "name": "Form template name",
        "field_name_1": "email",
        "field_name_2": "phone",
        "body": fake.paragraph(nb_sentences=5)
    }
    item_1 = {
        "name": "U1IT00001",
        "item_name": "Blender",
        "max_discount": "10%",
        "batch_number": "RR450020FRG",
        "price": 340,
        "category": "kitchen appliance"
    }

    item_2 = {
        "name": "U1IT00002",
        "item_name": "Egg",
        "category": "food",
        "quantity": 12,
        "price": 36,
        "item_description": "brown country eggs"
    }
    result = collection_name.insert_many([item_1, item_2, template1])
    assert result.acknowledged
    assert len(result.inserted_ids) == 3


def test_table(fill_db):
    dbname = get_database()

    collection_name = dbname["templates"]

    item_details = collection_name.find()
    all_data = []
    for item in item_details:
        all_data.append(item)
    assert len(all_data) == 4


def test_remove_collection(fill_db):
    dbname = get_database()

    collection_name = dbname["templates"]

    item_details = collection_name.find()
    all_data = []
    for item in item_details:
        all_data.append(item)
    assert len(all_data) > 0

    collection_name.delete_many({})
    item_details = collection_name.find()
    all_data = []
    for item in item_details:
        all_data.append(item)
    assert len(all_data) == 0


def test_select_documents(fill_db):
    dbname = get_database()
    collection_name = dbname["templates"]

    item_details = collection_name.find({"name": {'$exists': True}, "user_email": {'$exists': True}, })
    all_data = []
    for item in item_details:
        all_data.append(item)
    assert len(all_data) > 0

    collection_name.delete_many({})
    item_details = collection_name.find()
    all_data = []
    for item in item_details:
        all_data.append(item)
    assert len(all_data) == 0
