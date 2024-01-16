"""Main entrypoint for the API routes in of parma-analytics."""
import json
import logging
import os

from fastapi import Depends, FastAPI, HTTPException, status

from parma_mining.reddit.api.analytics_client import AnalyticsClient
from parma_mining.reddit.api.dependencies.auth import authenticate
from parma_mining.reddit.client import RedditClient
from parma_mining.reddit.model import CompaniesRequest, CompanyModel, DiscoveryModel

env = os.getenv("DEPLOYMENT_ENV", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()
reddit_client = RedditClient()
analytics_client = AnalyticsClient()


@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-reddit"}


@app.get("/initialize", status_code=200)
def initialize(source_id: int, token: str = Depends(authenticate)) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = reddit_client.initialize_normalization_map()
    # register the measurements to analytics
    normalization_map = analytics_client.register_measurements(
        token, normalization_map, source_module_id=source_id
    )[1]

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/companies",
    response_model=list[CompanyModel],
    status_code=status.HTTP_200_OK,
)
def get_company_info(
    companies: CompaniesRequest, token: str = Depends(authenticate)
) -> list[CompanyModel]:
    """Company details endpoint for the API."""
    all_comp_details = []
    for company_id, search_keys in companies.companies.items():
        for key in search_keys:
            search_list = companies.companies[company_id][key]
            for search_string in search_list:
                org_details = reddit_client.get_company_details(
                    search_str=search_string, company_id=company_id, search_type=key
                )
                all_comp_details.append(org_details)
    # feed the raw data to analytics
    for company in all_comp_details:
        try:
            analytics_client.feed_raw_data(token, company)
        except HTTPException as e:
            logger.error(
                f"Can't send crawling data for {company} to the Analytics: {e}"
            )
            raise HTTPException(
                f"Can't send crawling data for {company} to the Analytics: {e}"
            )
    return all_comp_details


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def discover_subreddits(
    query: str, token: str = Depends(authenticate)
) -> list[DiscoveryModel]:
    """Discovery endpoint for the API.

    (for reddit this endpoint enables searching for subreddits)
    """
    results = reddit_client.discover_subreddits(query)
    return results
