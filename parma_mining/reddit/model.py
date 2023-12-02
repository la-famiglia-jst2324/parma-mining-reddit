from datetime import datetime
from pydantic import BaseModel
from typing import List


class CommentModel(BaseModel):
    """Model to structure the JSON Data."""

    author: str
    text: str
    upvotes: int
    downvotes: int


class SubmissionModel(BaseModel):
    """Model to structure the JSON Data."""

    author: str
    comment_count: int
    comments: List[CommentModel]
    created_at: datetime
    edited: bool
    id: str
    is_original_content: bool
    is_self: bool
    is_video: bool
    over18: bool
    permalink: str
    scraped_at: datetime
    score: int
    subreddit_name: str
    subreddit_description: str
    subreddit_subscribers: int
    title: str
    text: str
    upvote_ratio: float
    url: str


class CompanyModel(BaseModel):
    name: str
    data_source: str
    submissions: List[SubmissionModel]
