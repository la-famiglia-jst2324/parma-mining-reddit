from unittest.mock import patch

import httpx
import pytest

from parma_mining.mining_common.const import HTTP_200, HTTP_500
from parma_mining.reddit.analytics_client import AnalyticsClient
from parma_mining.reddit.model import (
    CompanyModel,
    ResponseModel,
)

TOKEN = "mocked_token"


@pytest.fixture
def analytics_client():
    return AnalyticsClient()


@pytest.fixture
def mock_company_model():
    mock_company_data = {
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

    return CompanyModel(**mock_company_data)


@pytest.fixture
def mock_response_model(mock_company_model):
    return ResponseModel(
        source_name="TestSource",
        company_id="TestCompany",
        raw_data=mock_company_model,
    )


@patch("httpx.post")
def test_send_post_request_success(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"key": "value"})
    response = analytics_client.send_post_request(
        TOKEN, "http://example.com", {"data": "test"}
    )
    assert response == {"key": "value"}


@patch("httpx.post")
def test_send_post_request_failure(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_500, text="Internal Server Error")
    with pytest.raises(Exception) as exc_info:
        analytics_client.send_post_request(
            TOKEN, "http://example.com", {"data": "test"}
        )
    assert "API request failed" in str(exc_info.value)


@patch("httpx.post")
def test_register_measurements(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"id": "123"})
    mapping = {"Mappings": [{"DataType": "int", "MeasurementName": "test_metric"}]}
    result, updated_mapping = analytics_client.register_measurements(TOKEN, mapping)
    assert "source_measurement_id" in updated_mapping["Mappings"][0]
    assert result[0]["source_measurement_id"] == "123"


@patch("httpx.post")
def test_feed_raw_data(mock_post, analytics_client, mock_response_model):
    mock_post.return_value = httpx.Response(HTTP_200, json={"result": "success"})
    result = analytics_client.feed_raw_data(TOKEN, mock_response_model)
    assert result == {"result": "success"}
