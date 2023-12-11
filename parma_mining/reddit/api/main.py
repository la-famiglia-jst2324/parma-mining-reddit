"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI, HTTPException, status
from parma_mining.reddit.client import RedditClient
from parma_mining.reddit.model import CompanyModel, CompaniesRequest, DiscoveryModel
from parma_mining.reddit.api.analytics_client import AnalyticsClient
import json


app = FastAPI()
source_id = 1  # it is for now, we must formally define unniqe source module ids for all of our modules
reddit_client = RedditClient()
analytics_client = AnalyticsClient()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-reddit"}


# initialization endpoint
@app.get("/initialize", status_code=200)
def initialize() -> str:
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


@app.post(
    "/companies",
    response_model=list[CompanyModel],
    status_code=status.HTTP_200_OK,
)
def get_company_info(companies: CompaniesRequest) -> list[CompanyModel]:
    if not companies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Company list is empty!"
        )
    results = reddit_client.get_reddit_data(companies)
    return results


# @app.post(
#     "/organizations",
#     response_model=List[OrganizationModel],
#     status_code=status.HTTP_200_OK,
# )
# def get_organization_details(companies: CompaniesRequest) -> List[OrganizationModel]:
#     """Endpoint to get detailed information about a dict of organizations."""
#     all_org_details = []
#     for company_name, handles in companies.companies.items():
#         for handle in handles:
#             org_details = github_client.get_organization_details(handle)
#             all_org_details.append(org_details)

#     return all_org_details


# @app.get(
#     "/search/companies",
#     response_model=list[DiscoveryModel],
#     status_code=status.HTTP_200_OK,
# )
# def search_companies(query: str):
#     """Endpoint to search GitHub organizations based on a query."""
#     return github_client.search_organizations(query)
