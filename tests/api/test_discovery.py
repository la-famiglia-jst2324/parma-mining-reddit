from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200, HTTP_422
from parma_mining.mining_common.exceptions import ClientInvalidBodyError
from parma_mining.reddit.api.dependencies.auth import authenticate
from parma_mining.reddit.api.main import app
from parma_mining.reddit.model import DiscoveryRequest, DiscoveryResponse
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


@pytest.fixture
def mock_reddit_client(mocker) -> MagicMock:
    """Mocking RedditClient's discover method."""
    mock = mocker.patch("parma_mining.reddit.api.main.RedditClient.discover_subreddits")
    mock.return_value = DiscoveryResponse(urls=["mock_url"]).model_dump()
    return mock


# Test for successful discovery
def test_discover_endpoint_success(client: TestClient, mock_reddit_client: MagicMock):
    request_data = [
        DiscoveryRequest(company_id="123", name="TestCompany").model_dump(),
        DiscoveryRequest(company_id="456", name="AnotherCompany").model_dump(),
    ]

    response = client.post("/discover", json=request_data)
    assert response.status_code == HTTP_200
    assert isinstance(response.json(), dict)
    assert "identifiers" in response.json()
    assert "validity" in response.json()

    assert mock_reddit_client.called


def test_discover_endpoint_empty_request(client: TestClient):
    with pytest.raises(ClientInvalidBodyError) as exc_info:
        client.post("/discover", json=[])
    assert "Request body cannot be empty for discovery" in str(exc_info.value)


def test_discover_endpoint_invalid_format(client: TestClient):
    invalid_request_data = {"invalid": "data"}

    response = client.post("/discover", json=invalid_request_data)
    assert response.status_code == HTTP_422


def test_discover_non_existing_company(
    client: TestClient, mock_reddit_client: MagicMock
):
    mock_reddit_client.return_value = {}

    request_data = [
        DiscoveryRequest(company_id="999", name="NonExistingCompany").model_dump()
    ]
    response = client.post("/discover", json=request_data)

    assert response.status_code == HTTP_200
    response_data = response.json()
    assert response_data["identifiers"]["999"] == {"name": [], "subreddits": []}


def test_discover_endpoint_with_reddit_client_error(
    client: TestClient, mock_reddit_client: MagicMock
):
    mock_reddit_client.side_effect = Exception("Mocked Exception")
    request_data = [DiscoveryRequest(company_id="123", name="TestCompany").model_dump()]

    with pytest.raises(Exception) as exc_info:
        client.post("/discover", json=request_data)
    assert "Mocked Exception" in str(exc_info.value)
