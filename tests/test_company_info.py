import logging
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200, HTTP_404
from parma_mining.reddit.api.dependencies.auth import authenticate
from parma_mining.reddit.api.main import app
from parma_mining.reddit.model import CompanyModel
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


logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticsClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.reddit.api.main.AnalyticsClient.feed_raw_data")
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


@pytest.fixture
def mock_reddit_client(mocker) -> MagicMock:
    """Mocking the RedditClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.reddit.api.main.RedditClient.get_company_details")
    mock.return_value = CompanyModel.model_validate(
        {
            "id": "TestCompany",
            "search_key": "TestCompany",
            "search_type": "name",
            "data_source": "Reddit",
            "url": "https://reddit.com",
            "submissions": [
                {
                    "author": "TestAuthor",
                    "comment_count": 10,
                    "comments": [
                        {
                            "author": "TestAuthor",
                            "text": "TestComment",
                            "upvotes": 10,
                            "downvotes": 2,
                        }
                    ],
                    "created_at": "2021-01-01T00:00:00Z",
                    "id": "TestID",
                    "is_original_content": False,
                    "is_self": False,
                    "is_video": False,
                    "over18": False,
                    "permalink": "https://reddit.com",
                    "scraped_at": "2021-01-01T00:00:00Z",
                    "score": 10,
                    "subreddit_name": "TestSubreddit",
                    "subreddit_description": "TestDescription",
                    "subreddit_subscribers": 100,
                    "title": "TestTitle",
                    "text": "TestText",
                    "upvote_ratio": 0.5,
                    "url": "https://reddit.com",
                }
            ],
        }
    )
    return mock


def test_get_company_details(
    client: TestClient, mock_reddit_client: MagicMock, mock_analytics_client: MagicMock
):
    payload = {
        "companies": {
            "company1": {
                "name": ["company1_name"],
            },
            "company2": {
                "name": ["company2_name"],
                "domain": ["company2_domain"],
            },
        }
    }
    # this uses analytics_client.feed_raw_data too we need to mock that
    response = client.post("/companies", json=payload)
    mock_analytics_client.assert_called()
    assert response.status_code == HTTP_200


def test_get_company_details_bad_request(client: TestClient, mocker):
    mocker.patch(
        "parma_mining.reddit.api.main.RedditClient.get_company_details",
        side_effect=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        ),
    )

    payload = {
        "companies": {
            "company1": {
                "name": ["company1_name"],
            },
            "company2": {
                "name": ["company2_name"],
                "domain": ["company2_domain"],
            },
        }
    }

    response = client.post("/companies", json=payload)
    assert response.status_code == HTTP_404
