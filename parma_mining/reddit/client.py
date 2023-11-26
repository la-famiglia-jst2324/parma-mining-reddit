import praw
import json
from datetime import datetime
from dotenv import load_dotenv
import os


class RedditClient:
    def __init__(self):
        load_dotenv()
        reddit_api_key = os.getenv("REDDIT_API_KEY")
        self.reddit = praw.Reddit(
            client_id="JgHo7ALWRJWT2EX7wLmKtw",
            client_secret=reddit_api_key,
            user_agent="Startup_Data/1.0 (by /u/seyter61)",
        )
        self.data_source = "Reddit"
        self.data_source_url = "https://www.reddit.com/"
        self.results = {}

    def get_reddit_data(self, companies):
        query_set = {}
        for company in companies:
            results = self.reddit.subreddit("all").search(
                query=company, sort="relevance", time_filter="all", limit=10
            )
            query_set[company] = results

        result_set = {}
        for company, results in query_set.items():
            # creating the final dictionary
            item = {}
            # initialize necessary fields
            item["company"] = company
            item["data_source"] = self.data_source
            item["url"] = self.data_source_url
            item["submissions"] = []
            for submission in results:
                # collect comments
                submission.comments.replace_more(limit=10)
                all_comments = submission.comments.list()
                # create details dictionary about a submission
                submission_details = {
                    "author": submission.author.name
                    if submission.author
                    else "Unknown",
                    "comment_count": len(all_comments),
                    "comments": [
                        {
                            "author": comment.author.name
                            if comment.author
                            else "Unknown",
                            "text": comment.body,
                            "upvotes": str(comment.score),
                            "downvotes": str(comment.downs),
                        }
                        for comment in all_comments
                    ],
                    "createdAt": submission.created_utc,
                    "distinguished": submission.distinguished,
                    "edited": submission.edited,
                    "id": submission.id,
                    "is_original_content": submission.is_original_content,
                    "is_self": submission.is_self,
                    "is_video": submission.is_video,
                    "over18": submission.over_18,
                    "permalink": submission.permalink,
                    "scrapedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "score": submission.score,
                    "subreddit_name": submission.subreddit.display_name,
                    "subreddit_description": submission.subreddit.public_description,
                    "subreddit_subscribers": submission.subreddit.subscribers,
                    "title": submission.title,
                    "text": submission.selftext,
                    "upvote_ratio": submission.upvote_ratio,
                    "url": submission.url,
                }
                item["submissions"].append(submission_details)

            result_set[company] = item

        self.results = result_set

    def get_results(self):
        return self.results

    def print_results(self):
        result_json = json.dumps(self.results, indent=4)
        print(result_json)
