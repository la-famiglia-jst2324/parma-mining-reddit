"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI, HTTPException, status
from typing import List
from parma_mining.reddit.client import RedditClient

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-reddit"}


@app.post("/get_reddit_data", status_code=status.HTTP_200_OK)
def get_reddit_data(companies: List[str]) -> dict:
    if not companies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Company list is empty!"
        )
    reddit_client = RedditClient()
    results = reddit_client.get_reddit_data(companies)
    return {"results": results}
