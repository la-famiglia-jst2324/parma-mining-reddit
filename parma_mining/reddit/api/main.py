"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI, HTTPException, status
from parma_mining.reddit.client import RedditClient
from parma_mining.reddit.model import CompanyModel, CompaniesRequest, DiscoveryModel
from parma_mining.reddit.api.analytics_client import AnalyticsClient
from typing import List, Dict, Optional
import json

app = FastAPI()
reddit_client = RedditClient()
analytics_client = AnalyticsClient()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-reddit"}


# initialization endpoint
@app.get("/initialize", status_code=200)
def initialize(source_id: int) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = reddit_client.initialize_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


# get company details endpoint
@app.post(
    "/companies",
    response_model=List[CompanyModel],
    status_code=status.HTTP_200_OK,
)
def get_company_info(companies: CompaniesRequest) -> List[CompanyModel]:
    all_org_details = []
    for company_id, search_keys in companies.companies.items():
        for key in search_keys:
            search_list = companies.companies[company_id][key]
            for search_string in search_list:
                org_details = reddit_client.get_company_details(
                    search_str=search_string, company_id=company_id, search_type=key
                )
                all_org_details.append(org_details)

    return all_org_details


# discovery endpoint ( for reddit this endpoint enables searching for subreddits)
@app.get(
    "/discover",
    response_model=List[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def discover_subreddits(query: str) -> List[DiscoveryModel]:
    """Discovery endpoint for the API."""
    results = reddit_client.discover_subreddits(query)
    return results
