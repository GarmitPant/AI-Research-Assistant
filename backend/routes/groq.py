from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import Optional

router = APIRouter()

class GroqRequest(BaseModel):
    prompt: str
    content: Optional[str] = ""

class GroqResponse(BaseModel):
    output: str

@router.post("/groq", response_model=GroqResponse)
async def process_with_groq(request: GroqRequest):
    """
    Process content with Groq LLM API and return the response
    """
    try:
        # Get API key from environment variables
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="Groq API key not configured"
            )
        
        # Prepare the system message and user prompt
        system_message = """You are a helpful research assistant. Your task is to provide accurate, 
        concise, and relevant information. Focus on answering the user's query directly and factually.
        If you don't have enough information to answer the query, acknowledge this limitation.
        Provide well-structured responses with clear organization and formatting when appropriate.
        Use bullet points or numbered lists for complex information when it improves readability."""
        
        # Create user message with just the prompt
        user_message = f"User Query: {request.prompt}"
        
        # Add instructions based on whether content is provided
        if request.content and request.content.strip():
            user_message += f"""
            
            Web Content:
            {request.content}
            
            Please provide a well-structured, factual response to the query based on the web content.
            """
        else:
            user_message += """
            
            Please provide a well-structured, factual response to the query based on your knowledge.
            """
        
        # Prepare the API request
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Choose model - LLaMA3 or Mixtral
        model = "llama3-8b-8192" # Alternative: "mixtral-8x7b-32768"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.3,
            "max_tokens": 2048
        }
        
        # Make the API request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=60)
            
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Groq API error: {response.text}"
            )
        
        # Extract the LLM response
        response_data = response.json()
        llm_response = response_data["choices"][0]["message"]["content"]
        
        return GroqResponse(output=llm_response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing with Groq: {str(e)}"
        )
