"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI, HTTPException, status
from parma_mining.reddit.client import RedditClient
from parma_mining.reddit.model import CompanyModel
import json

app = FastAPI()

reddit_client = RedditClient()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-reddit"}


# initialization endpoint
@app.get("/initialize", status_code=200)
def initialize() -> str:
    """Initialization endpoint for the API."""
    return json.dumps(reddit_client.initialize_normalization_map())


# company info endpoint
@app.post("/get_company_info", status_code=status.HTTP_200_OK)
def get_company_info(companies: list[str]) -> list[CompanyModel]:
    if not companies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Company list is empty!"
        )
    # use the client initialized in the init endpoint
    results = reddit_client.get_reddit_data(companies)
    return results
