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


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticsClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.reddit.api.main.AnalyticsClient.feed_raw_data")
    mock = mocker.patch(
        "parma_mining.reddit.api.main.AnalyticsClient.crawling_finished"
    )
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


@pytest.fixture
def mock_reddit_client(mocker) -> MagicMock:
    """Mocking the RedditClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.reddit.api.main.RedditClient.get_company_details")
    mock.return_value = CompanyModel.model_validate(
        {
            "name": "test company",
            "searches": [
                {"subreddit": "startups", "submissions": []},
                {
                    "subreddit": "all",
                    "submissions": [
                        {
                            "author": "test author",
                            "comment_count": 1,
                            "comments": [
                                {
                                    "author": "test author",
                                    "text": "comment",
                                    "upvotes": 2,
                                    "downvotes": 0,
                                }
                            ],
                            "created_at": "2018-11-29 09:05:06+00:00",
                            "id": "12",
                            "is_original_content": False,
                            "is_self": True,
                            "is_video": False,
                            "over18": False,
                            "permalink": "/test/permalink",
                            "scraped_at": "2024-01-22 19:31:24.384102+00:00",
                            "score": 29,
                            "subreddit_name": "test subreddit",
                            "subreddit_description": "test description",
                            "subreddit_subscribers": 2,
                            "title": "test title",
                            "text": "test text",
                            "upvote_ratio": 0.89,
                            "url": "test_url",
                        }
                    ],
                },
            ],
        }
    )

    return mock


def test_get_company_details(
    client: TestClient, mock_reddit_client: MagicMock, mock_analytics_client: MagicMock
):
    payload = {
        "task_id": 123,
        "companies": {
            "company1": {
                "name": ["company1_name"],
            },
            "company2": {
                "name": ["company2_name"],
                "domain": ["company2_domain"],
            },
        },
    }
    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)
    mock_analytics_client.assert_called()
    assert response.status_code == HTTP_200


def test_get_company_details_bad_request(client: TestClient, mocker):
    mocker.patch(
        "parma_mining.reddit.api.main.RedditClient.get_company_details",
        side_effect=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        ),
    )

    payload = {
        "task_id": 123,
        "companies": {
            "company1": {
                "name": ["company1_name"],
            },
            "company2": {
                "name": ["company2_name"],
            },
        },
    }

    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)
    assert response.status_code == HTTP_404
