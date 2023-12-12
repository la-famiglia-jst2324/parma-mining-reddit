import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from starlette import status
from unittest.mock import MagicMock
from parma_mining.reddit.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_reddit_client(mocker) -> MagicMock:
    """Mocking the RedditClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.reddit.api.main.RedditClient.get_company_details")
    mock.return_value = {
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
    return mock


def test_get_company_details(mock_reddit_client: MagicMock):
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

    assert response.status_code == 200

    assert response.json() == [
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
        },
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
        },
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
        },
    ]


def test_get_organization_details_bad_request(mocker):
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
    assert response.status_code == 404
