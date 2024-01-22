"""Main entrypoint for the API routes in of parma-analytics."""
import json
import logging
import os
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, status

from parma_mining.mining_common.exceptions import (
    AnalyticsError,
    ClientInvalidBodyError,
    CrawlingError,
)
from parma_mining.mining_common.helper import collect_errors
from parma_mining.reddit.analytics_client import AnalyticsClient
from parma_mining.reddit.api.dependencies.auth import authenticate
from parma_mining.reddit.client import RedditClient
from parma_mining.reddit.model import (
    CompaniesRequest,
    CrawlingFinishedInputModel,
    DiscoveryRequest,
    ErrorInfoModel,
    FinalDiscoveryResponse,
    ResponseModel,
)
from parma_mining.reddit.normalization_map import RedditNormalizationMap

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
normalization = RedditNormalizationMap()


@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-reddit"}


@app.get("/dummy-auth", status_code=status.HTTP_200_OK)
def dummy_auth(token: str = Depends(authenticate)):
    """Dummy endpoint.

    This endpoint is used to demonstrate the usage of authenticate function. This
    function ensures that the incoming request comes from the analytics. token variable
    can be used to make requests to analytics.
    """
    logger.debug("Dummy endpoint called")
    return {"welcome": "at parma-mining-crunchbase"}


@app.get("/initialize", status_code=200)
def initialize(source_id: int, token: str = Depends(authenticate)) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = normalization.get_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        token, normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_company_details(body: CompaniesRequest, token: str = Depends(authenticate)):
    """Endpoint to get detailed information about a dict of company."""
    errors: dict[str, ErrorInfoModel] = {}
    subreddits = ["all"]
    for company_id, company_data in body.companies.items():
        for data_type, handles in company_data.items():
            if "subreddits" in company_data:
                if len(company_data["subreddits"]) > 0:
                    subreddits = company_data["subreddits"]
            for handle in handles:
                print(data_type)
                if data_type == "name":
                    try:
                        comp_details = reddit_client.get_company_details(
                            search_str=handle, subreddit=subreddits, time_filter="all"
                        )
                        print(comp_details.updated_model_dump())
                    except CrawlingError as e:
                        logger.error(
                            f"Can't fetch company details from GitHub. Error: {e}"
                        )
                        collect_errors(company_id, errors, e)
                        continue
                    data = ResponseModel(
                        source_name="reddit",
                        company_id=company_id,
                        raw_data=comp_details,
                    )
                    # Write data to db via endpoint in analytics backend
                    try:
                        analytics_client.feed_raw_data(token, data)
                    except AnalyticsError as e:
                        logger.error(
                            f"Can't send crawling data to the Analytics. Error: {e}"
                        )
                        collect_errors(company_id, errors, e)

                else:
                    msg = f"Unsupported type error for {data_type} in {handle}"
                    logger.error(msg)
                    collect_errors(company_id, errors, ClientInvalidBodyError(msg))

    return analytics_client.crawling_finished(
        token,
        json.loads(
            CrawlingFinishedInputModel(
                task_id=body.task_id, errors=errors
            ).model_dump_json()
        ),
    )


@app.post(
    "/discover",
    response_model=FinalDiscoveryResponse,
    status_code=status.HTTP_200_OK,
)
def discover_subreddits(
    request: list[DiscoveryRequest], token: str = Depends(authenticate)
):
    """Endpoint to discover subreddits based on provided names."""
    if not request:
        msg = "Request body cannot be empty for discovery"
        logger.error(msg)
        raise ClientInvalidBodyError(msg)
    subreddits_length = 2
    response_data = {}
    for company in request:
        logger.debug(
            f"Discovering with name: {company.name} for company_id {company.company_id}"
        )
        response = reddit_client.discover_subreddits(company.name, subreddits_length)
        response_data[company.company_id] = response

    current_date = datetime.now()
    valid_until = current_date + timedelta(days=180)

    return FinalDiscoveryResponse(identifiers=response_data, validity=valid_until)
