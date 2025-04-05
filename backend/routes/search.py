from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import httpx
import os
from typing import List

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

class SearchResults(BaseModel):
    links: List[str]

@router.post("/search", response_model=SearchResults)
async def search(query: SearchQuery):
    """
    Search for relevant URLs using Google Custom Search API
    """
    try:
        # Get API key and search engine ID from environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        if not api_key or not search_engine_id:
            raise HTTPException(
                status_code=500, 
                detail="Google API credentials not configured"
            )
        
        # Prepare the API request
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query.query,
            "num": 5  # Get top 5 results
        }
        
        # Make the API request
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Google API error: {response.text}"
            )
        
        # Extract URLs from the response
        search_results = response.json()
        links = []
        
        if "items" in search_results:
            for item in search_results["items"]:
                links.append(item["link"])
        
        return SearchResults(links=links)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during search: {str(e)}"
        )
