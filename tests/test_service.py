from fastapi.testclient import TestClient

from app.core.config import settings
from tests import fill_db


def test_get_forms_without_params(mocked_session_client: TestClient) -> None:
    r = mocked_session_client.post(f"{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_forms")
    assert r.status_code == 406


def test_get_forms_duplicated_params(mocked_session_client: TestClient) -> None:
    r = mocked_session_client.post(
        f"{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_forms?"
        f"field_1=hello&field_1=ivanov@gmail.com")
    assert r.status_code == 409


def test_get_forms_field_email(mocked_session_client: TestClient) -> None:
    field_name = "field_1"
    r = mocked_session_client.post(
        f"{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_forms?"
        f"{field_name}=ivanov@gmail.com")
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 1
    assert content[field_name] == "email"


def test_get_forms_field_bad_email(mocked_session_client: TestClient) -> None:
    field_name = "field_1"
    r = mocked_session_client.post(
        f"{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_forms?"
        f"{field_name}=@ivanov@gmail.com")
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 1
    assert content[field_name] == "text"


def test_get_forms_email_text(fill_db, mocked_session_client: TestClient) -> None:
    field_email = "user_email"
    field_text = "user_phone"
    r = mocked_session_client.post(
        f'{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_forms?'
        f'{field_email}=ivanov@gmail.com&{field_text}="+7 123 456 78 90"')
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 2
    assert content[field_email] == "email"
    assert content[field_text] == "text"


def test_get_forms_email_phone(fill_db, mocked_session_client: TestClient) -> None:
    field_email = "user_email"
    field_phone = "user_phone"
    r = mocked_session_client.post(
        f'{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_forms?'
        f'{field_email}=ivanov@gmail.com&{field_phone}=%2B7%20123%20456%2078%2090')
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 2
    assert content[field_email] == "email"
    assert content[field_phone] == "phone"


def test_get_forms_good_one_form(fill_db, mocked_session_client: TestClient) -> None:
    r = mocked_session_client.post(
        f'{settings.SERVER_HOST}:{settings.SERVER_PORT}'
        f'/get_forms?'
        f'user_email=ivanov@gmail.com&user_phone=%2B7%20123%20456%2078%2090&user_info=Тест')
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 1
    assert content[0] == "FormOrder"


def test_get_forms_good_two_forms(fill_db, mocked_session_client: TestClient) -> None:
    r = mocked_session_client.post(
        f'{settings.SERVER_HOST}:{settings.SERVER_PORT}'
        f'/get_forms?'
        f'user_email=ivanov@gmail.com&user_phone=%2B7%20123%20456%2078%2090&user_info=Тест1&user_answer=Тест2')
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 2
    assert "FormOrder" in content
    assert "FormAnswer" in content
