import praw
from datetime import datetime
from dotenv import load_dotenv
import os
from parma_mining.reddit.model import CompanyModel, SubmissionModel, CommentModel
from parma_mining.reddit.normalization_map import RedditNormalizationMap
from typing import List, Dict, Union


class RedditClient:
    normalization_map: Dict[
        str, Union[str, List[Dict[str, Union[str, List[Dict[str, Union[str, str]]]]]]]
    ] = {}

    def __init__(self):
        load_dotenv()
        reddit_api_key = str(os.getenv("REDDIT_API_KEY") or "")
        reddit_client_id = str(os.getenv("REDDIT_CLIENT_ID") or "")
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_api_key,
            user_agent="Startup_Data/1.0 (by /u/seyter61)",
        )
        self.data_source = "Reddit"
        self.data_source_url = str(os.getenv("REDDIT_BASE_URL") or "")
        self.results = {}

    def initialize_normalization_map(self) -> dict:
        self.normalization_map = RedditNormalizationMap().get_normalization_map()
        return self.normalization_map

    def get_reddit_data(self, companies: list) -> list[CompanyModel]:
        query_set = {}
        for company in companies:
            results = self.reddit.subreddit("all").search(
                query=company, sort="relevance", time_filter="all", limit=10
            )
            query_set[company] = results
        companies = []
        for company, results in query_set.items():
            # creating the company model
            company_info = {
                "name": company,
                "data_source": self.data_source,
                "url": self.data_source_url,
                "submissions": [],
            }
            for submission in results:
                # collect comments
                submission.comments.replace_more(limit=10)
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
                        "edited": submission.edited,
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
                        "subreddit_description": submission.subreddit.public_description,
                        "subreddit_subscribers": submission.subreddit.subscribers,
                        "title": submission.title,
                        "text": submission.selftext,
                        "upvote_ratio": submission.upvote_ratio,
                        "url": submission.url,
                    }
                )
                company_info["submissions"].append(submission_details)

            companies.append(CompanyModel.model_validate(company_info))

        return companies

    def assign_ids(self, mapping, parent_id=None, current_id=1):
        result = []

        for field_mapping in mapping["Mappings"]:
            measurement_id = current_id
            measurement = {
                "id": measurement_id,
                "parent_id": parent_id,
                "type": field_mapping["DataType"],
                "measurement_name": field_mapping["MeasurementName"],
            }

            if "NestedMappings" in field_mapping:
                nested_measurements, current_id = self.assign_ids(
                    {"Mappings": field_mapping["NestedMappings"]},
                    parent_id=measurement_id,
                    current_id=current_id + 1,
                )
                result.extend(nested_measurements)

            result.append(measurement)
            current_id += 1

        return result, current_id
