"""Main entrypoint for the API routes in of parma-analytics."""
import json

from fastapi import FastAPI, HTTPException, status

from parma_mining.reddit.api.analytics_client import AnalyticsClient
from parma_mining.reddit.client import RedditClient
from parma_mining.reddit.model import CompaniesRequest, DiscoveryModel
from parma_mining.reddit.normalization_map import RedditNormalizationMap

app = FastAPI()
reddit_client = RedditClient()
analytics_client = AnalyticsClient()
normalization = RedditNormalizationMap()


@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-reddit"}


@app.get("/initialize", status_code=200)
def initialize(source_id: int) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = normalization.get_normalization_map()
    # register the measurements to analytics
    normalization_map = analytics_client.register_measurements(
        normalization_map, source_module_id=source_id
    )[1]

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_organization_details(companies: CompaniesRequest):
    """Company details endpoint for the API."""
    # time_filter – Can be one of: "all", "day", "hour", "month", "week", or "year".
    time_filter = "all"
    subreddit = "all"
    options = [subreddit, time_filter]
    all_comp_details = []
    for company_id, search_keys in companies.companies.items():
        for key in search_keys:
            search_list = companies.companies[company_id][key]
            for search_string in search_list:
                org_details = reddit_client.get_company_details(
                    search_str=search_string,
                    company_id=company_id,
                    search_type=key,
                    options=options,
                )
                all_comp_details.append(org_details)
    # feed the raw data to analytics
    for company in all_comp_details:
        try:
            analytics_client.feed_raw_data(company)
        except HTTPException:
            raise HTTPException("Can't send crawling data to the Analytics.")

    analytics_client.finish_crawling("success")
    return "done"


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def discover_subreddits(query: str) -> list[DiscoveryModel]:
    """Discovery endpoint for the API.

    (for reddit this endpoint enables searching for subreddits)
    """
    results = reddit_client.discover_subreddits(query)
    return results
