"""Reddit client for fetching data from Reddit API."""
import logging
import os
from datetime import datetime

import praw
from dotenv import load_dotenv

from parma_mining.mining_common.exceptions import ClientError, CrawlingError
from parma_mining.reddit.model import (
    CommentModel,
    CompanyModel,
    DiscoveryResponse,
    SearchModel,
    SubmissionModel,
)

logger = logging.getLogger(__name__)


class RedditClient:
    """Client class for fetching data from Reddit API."""

    def __init__(self):
        """Initialize the Reddit client."""
        load_dotenv()
        reddit_api_key = str(os.getenv("REDDIT_API_KEY") or "")
        reddit_client_id = str(os.getenv("REDDIT_CLIENT_ID") or "")
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_api_key,
            user_agent="Parma_Mining_Reddit/1.0",
        )
        self.data_source = "reddit"
        self.data_source_url = str(os.getenv("REDDIT_BASE_URL") or "")
        self.results = {}

    def get_company_details(
        self, search_str: str, subreddit: list[str], time_filter: str
    ) -> CompanyModel:
        """Get company details from Reddit API."""
        # time_filter – Can be one of: "all", "day", "hour", "month", "week", or "year"
        try:
            searches = []
            company_info = {
                "name": search_str,
                "searches": [],
            }
            for sub in subreddit:
                results = self.reddit.subreddit(sub).search(
                    query=search_str, sort="relevance", time_filter=time_filter, limit=5
                )
                submissions = []
                search_info = {
                    "subreddit": sub,
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
                                "author": comment.author.name
                                if comment.author
                                else "Unknown",
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
                            "scraped_at": datetime.utcnow().strftime(
                                "%Y-%m-%dT%H:%M:%S.%fZ"
                            ),
                            "score": submission.score,
                            "subreddit_name": submission.subreddit.display_name,
                            "subreddit_description": (
                                submission.subreddit.public_description
                            ),
                            "subreddit_subscribers": submission.subreddit.subscribers,
                            "title": submission.title,
                            "text": submission.selftext,
                            "upvote_ratio": submission.upvote_ratio,
                            "url": submission.url,
                        }
                    )
                    # typecast to list
                    submissions.append(submission_details)
                search_info["submissions"] = submissions
                searches.append(SearchModel.model_validate(search_info))

            company_info["searches"] = searches
            return CompanyModel.model_validate(company_info)

        except Exception as e:
            msg = f"Error fetching organization details for {search_str}: {e}"
            logger.error(msg)
            raise CrawlingError(msg)

    def discover_subreddits(self, query: str, length: int) -> DiscoveryResponse:
        """Discover subreddits from Reddit API."""
        try:
            search_results = self.reddit.subreddits.search(query=query, limit=10)
            subreddits = []
            for subreddit in search_results:
                # at most x subreddits
                subreddits.append(subreddit.display_name)
                if len(subreddits) == length:
                    break
            return DiscoveryResponse.model_validate(
                {"subreddits": subreddits, "name": [query]}
            )

        except Exception as e:
            msg = f"Error searching organizations for {query}: {e}"
            logger.error(msg)
            raise ClientError()
