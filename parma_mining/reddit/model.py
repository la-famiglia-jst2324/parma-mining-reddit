"""Pydantic models for Reddit data."""
import json
from datetime import datetime

from pydantic import BaseModel


class CommentModel(BaseModel):
    """Comment model for Reddit data."""

    author: str | None
    text: str | None
    upvotes: int | None
    downvotes: int | None


class SubmissionModel(BaseModel):
    """Submission model for Reddit data."""

    author: str | None
    comment_count: int | None
    comments: list[CommentModel] | None
    created_at: datetime | None
    id: str | None
    is_original_content: bool | None
    is_self: bool | None
    is_video: bool | None
    over18: bool | None
    permalink: str | None
    scraped_at: datetime | None
    score: int | None
    subreddit_name: str | None
    subreddit_description: str | None
    subreddit_subscribers: int | None
    title: str | None
    text: str | None
    upvote_ratio: float | None
    url: str | None


class SearchModel(BaseModel):
    """Search model for Reddit data."""

    subreddit: str | None
    submissions: list[SubmissionModel] | None


class CompanyModel(BaseModel):
    """Company model for Reddit data."""

    name: str | None
    searches: list[SearchModel] | None

    def updated_model_dump(self) -> str:
        """Dump the CompanyModel instance to a JSON string."""
        # Convert datetime objects to string representation
        json_serializable_dict = self.model_dump()
        subs = []
        if self.searches:
            for search in self.searches:
                if search.submissions:
                    for sub in search.submissions:
                        if sub:
                            subs.append(sub.model_dump())
                json_serializable_dict["submissions"] = subs
        return json.dumps(json_serializable_dict, default=str)


class CompaniesRequest(BaseModel):
    """Companies request model for Reddit data."""

    task_id: int
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    """Response model for Reddit  data."""

    source_name: str
    company_id: str
    raw_data: CompanyModel


class DiscoveryRequest(BaseModel):
    """Request model for the discovery endpoint."""

    company_id: str
    name: str


class DiscoveryResponse(BaseModel):
    """Define the output model for the discovery endpoint."""

    subreddits: list[str] = []
    name: list[str] = []


class FinalDiscoveryResponse(BaseModel):
    """Define the final discovery response model."""

    identifiers: dict[str, DiscoveryResponse]
    validity: datetime


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str | None


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None
