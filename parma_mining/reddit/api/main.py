"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI, HTTPException
from typing import List
from parma_mining.reddit.client import RedditClient

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-reddit"}


@app.post("/get_reddit_data")
def get_reddit_data(companies: List[str]):
    if not companies:
        raise HTTPException(status_code=400, detail="Company list is empty")
    reddit_client = RedditClient()
    reddit_client.get_reddit_data(companies)
    results = reddit_client.get_results()
    return {"results": results}
