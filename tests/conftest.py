import pytest

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def mocked_session_client(request):
    client = TestClient(app, raise_server_exceptions=False)
    yield client
