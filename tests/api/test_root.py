from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200, HTTP_405
from parma_mining.reddit.api.main import app

client = TestClient(app)


def test_root_success():
    response = client.get("/")
    assert response.status_code == HTTP_200
    assert response.json() == {"welcome": "at parma-mining-reddit"}


def test_root_method_not_allowed():
    response = client.post("/")
    assert response.status_code == HTTP_405
