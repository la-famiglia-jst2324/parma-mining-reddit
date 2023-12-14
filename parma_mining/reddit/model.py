import json
from datetime import datetime

from pydantic import BaseModel


class CommentModel(BaseModel):
    """Model to structure the JSON Data."""

    author: str | None
    text: str | None
    upvotes: int | None
    downvotes: int | None


class SubmissionModel(BaseModel):
    """Model to structure the JSON Data."""

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


class CompanyModel(BaseModel):
    id: str | None
    search_key: str | None  # generally the name of the company, sometimes domain
    search_type: str | None  # "name" or "domain" or another type
    data_source: str | None
    url: str | None
    submissions: list[SubmissionModel] | None

    def updated_model_dump(self) -> str:
        """Dump the CompanyModel instance to a JSON string."""
        # Convert datetime objects to string representation
        json_serializable_dict = self.model_dump()
        subs = []
        if self.submissions:
            for sub in self.submissions:
                if sub:
                    subs.append(sub.model_dump())
        json_serializable_dict["submissions"] = subs

        return json.dumps(json_serializable_dict, default=str)


class DiscoveryModel(BaseModel):
    name: str | None
    url: str | None


class CompaniesRequest(BaseModel):
    companies: dict[str, dict[str, list[str]]]
