from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
from typing import List
import re
from requests_html import HTMLSession

router = APIRouter()

class ScrapeRequest(BaseModel):
    links: List[str]

class ScrapeResponse(BaseModel):
    content: str

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest):
    """
    Scrape content from a list of URLs and return cleaned text
    """
    try:
        if not request.links:
            return ScrapeResponse(content="No links provided to scrape.")
        
        all_content = []
        
        # Create a session for requests-html
        session = HTMLSession()
        
        for url in request.links:
            try:
                # Get the page content
                response = session.get(url, timeout=10)
                
                # Render JavaScript if needed
                if "javascript" in response.text.lower() or "dynamic" in response.text.lower():
                    response.html.render(timeout=20)
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.html.html, 'html.parser')
                
                # Remove script, style, and other non-content elements
                for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'iframe', 'noscript']):
                    element.decompose()
                
                # Extract text from paragraphs, headings, and list items
                content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
                
                # Get text from each element
                content = []
                for element in content_elements:
                    text = element.get_text().strip()
                    if text and len(text) > 20:  # Filter out short fragments
                        content.append(text)
                
                # Join the text with newlines
                page_content = "\n\n".join(content)
                
                # Clean up the text
                page_content = re.sub(r'\s+', ' ', page_content)  # Replace multiple spaces with a single space
                page_content = re.sub(r'\n\s*\n', '\n\n', page_content)  # Remove empty lines
                
                # Add source information
                all_content.append(f"Source: {url}\n\n{page_content}\n\n{'='*50}\n")
            
            except Exception as e:
                all_content.append(f"Failed to scrape {url}: {str(e)}\n\n")
                continue
        
        # Combine all content
        combined_content = "\n".join(all_content)
        
        # Limit content length if needed (e.g., for LLM token limits)
        if len(combined_content) > 100000:
            combined_content = combined_content[:100000] + "...[content truncated due to length]"
        
        return ScrapeResponse(content=combined_content)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during scraping: {str(e)}"
        )
    finally:
        # Close the session
        if 'session' in locals():
            session.close()
