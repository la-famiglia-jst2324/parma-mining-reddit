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
    mock = mocker.patch("parma_mining.reddit.api.main.RedditClient.get_reddit_data")
    mock.return_value = [
        {
            "name": "TestCompany",
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
                    "edited": False,
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
    ]
    return mock


# test for following endpoint
# '@app.post("/get_company_info", status_code=status.HTTP_200_OK)
# def get_company_info(companies: List[str]) -> list:
#     if not companies:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Company list is empty!"
#         )
#     # use the client initialized in the init endpoint
#     results = reddit_client.get_reddit_data(companies)
#     return results'


def test_get_company_info(mock_reddit_client: MagicMock):
    # give list of companies as argument of the post request
    response = client.post("/get_company_info", json=["TestCompany"])

    assert response.status_code == 200

    assert response.json() == [
        {
            "name": "TestCompany",
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
                    "edited": False,
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
    ]


def test_get_reddit_data_bad_request(mocker):
    mocker.patch(
        "parma_mining.reddit.api.main.RedditClient.get_reddit_data",
        side_effect=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Company list is empty!"
        ),
    )

    response = client.get("/organization/notExisting")
    assert response.status_code == 404
