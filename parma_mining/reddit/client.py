import os
from datetime import datetime

import praw
from dotenv import load_dotenv

from parma_mining.reddit.model import (
    CommentModel,
    CompanyModel,
    DiscoveryModel,
    SubmissionModel,
)
from parma_mining.reddit.normalization_map import RedditNormalizationMap


class RedditClient:
    normalization_map: dict[
        str, str | list[dict[str, str | list[dict[str, str | str]]]]
    ] = {}

    def __init__(self):
        load_dotenv()
        reddit_api_key = str(os.getenv("REDDIT_API_KEY") or "")
        reddit_client_id = str(os.getenv("REDDIT_CLIENT_ID") or "")
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_api_key,
            user_agent="Startup_Data/1.0",
        )
        self.data_source = "Reddit"
        self.data_source_url = str(os.getenv("REDDIT_BASE_URL") or "")
        self.results = {}

    def initialize_normalization_map(self) -> dict:
        self.normalization_map = RedditNormalizationMap().get_normalization_map()
        return self.normalization_map

    def get_company_details(
        self, search_str: str, company_id: str, search_type: str, subreddit="all"
    ) -> CompanyModel:
        results = self.reddit.subreddit(subreddit).search(
            query=search_str, sort="relevance", time_filter="all", limit=5
        )
        submissions = []
        company_info = {
            "id": company_id,
            # generally the name of the company, sometimes domain
            "search_key": search_str,
            # "name" or "domain" or another type
            "search_type": search_type,
            "data_source": self.data_source,
            "url": self.data_source_url,
            "submissions": [],
        }
        for submission in results:
            # collect comments
            submission.comments.replace_more(limit=2)
            all_comments = submission.comments.list()
            # get the comments and store them in a list
            comments = []
            for comment in all_comments:
                comment_details = CommentModel.model_validate(
                    {
                        "author": comment.author.name if comment.author else "Unknown",
                        "text": comment.body,
                        "upvotes": comment.score,
                        "downvotes": comment.downs,
                    }
                )
                comments.append(comment_details)
            # model for submission
            submission_details = SubmissionModel.model_validate(
                {
                    "author": submission.author.name
                    if submission.author
                    else "Unknown",
                    "comment_count": len(all_comments),
                    "comments": comments,
                    "created_at": datetime.utcfromtimestamp(
                        submission.created_utc
                    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "id": submission.id,
                    "is_original_content": submission.is_original_content,
                    "is_self": submission.is_self,
                    "is_video": submission.is_video,
                    "over18": submission.over_18,
                    "permalink": submission.permalink,
                    "scraped_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "score": submission.score,
                    "subreddit_name": submission.subreddit.display_name,
                    "subreddit_description": submission.subreddit.public_description,
                    "subreddit_subscribers": submission.subreddit.subscribers,
                    "title": submission.title,
                    "text": submission.selftext,
                    "upvote_ratio": submission.upvote_ratio,
                    "url": submission.url,
                }
            )
            # typecast to list
            submissions.append(submission_details)
        company_info["submissions"] = submissions

        return CompanyModel.model_validate(company_info)

    def discover_subreddits(self, query: str) -> list[DiscoveryModel]:
        results = self.reddit.subreddits.search(query=query, limit=10)
        return [
            DiscoveryModel.model_validate(
                {"name": subreddit.display_name, "url": subreddit.url}
            )
            for subreddit in results
        ]
