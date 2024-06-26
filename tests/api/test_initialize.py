from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200, HTTP_422
from parma_mining.reddit.api.dependencies.auth import authenticate
from parma_mining.reddit.api.main import app
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
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticsClient's register_measurements method."""
    mock = mocker.patch(
        "parma_mining.reddit.api.main.AnalyticsClient.register_measurements"
    )
    return mock


def test_initialize_success(client: TestClient, mock_analytics_client: MagicMock):
    response = client.get("/initialize?source_id=123")
    assert response.status_code == HTTP_200
    mock_analytics_client.assert_called_once()


def test_initialize_missing_source_id(client: TestClient):
    response = client.get("/initialize")
    assert response.status_code == HTTP_422
