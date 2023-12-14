from datetime import datetime
import json
from pydantic import BaseModel
from typing import List, Dict, Optional


class CommentModel(BaseModel):
    """Model to structure the JSON Data."""

    author: Optional[str]
    text: Optional[str]
    upvotes: Optional[int]
    downvotes: Optional[int]


class SubmissionModel(BaseModel):
    """Model to structure the JSON Data."""

    author: Optional[str]
    comment_count: Optional[int]
    comments: Optional[List[CommentModel]]
    created_at: Optional[datetime]
    id: Optional[str]
    is_original_content: Optional[bool]
    is_self: Optional[bool]
    is_video: Optional[bool]
    over18: Optional[bool]
    permalink: Optional[str]
    scraped_at: Optional[datetime]
    score: Optional[int]
    subreddit_name: Optional[str]
    subreddit_description: Optional[str]
    subreddit_subscribers: Optional[int]
    title: Optional[str]
    text: Optional[str]
    upvote_ratio: Optional[float]
    url: Optional[str]


class CompanyModel(BaseModel):
    id: Optional[str]
    search_key: Optional[str]  # generally the name of the company, sometimes domain
    search_type: Optional[str]  # "name" or "domain" or another type
    data_source: Optional[str]
    url: Optional[str]
    submissions: Optional[list[SubmissionModel]]

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
    name: Optional[str]
    url: Optional[str]


class CompaniesRequest(BaseModel):
    companies: Dict[str, Dict[str, List[str]]]
