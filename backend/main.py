from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
import uvicorn
import os
from dotenv import load_dotenv

# Import route modules
from routes import search, scrape, groq, email, auth

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Research Assistant API")

# Configure Session Middleware (must be added before CORS)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "a_secure_random_string_for_session_encryption"),
    max_age=3600,  # 1 hour
    same_site="lax",  # Changed from "none" to "lax" for better compatibility
    https_only=False,  # Set to True in production with HTTPS
    session_cookie="session"  # Explicitly name the cookie
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(scrape.router, prefix="/api", tags=["scrape"])
app.include_router(groq.router, prefix="/api", tags=["groq"])
app.include_router(email.router, prefix="/api", tags=["email"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def redirect_to_docs():
    return "/docs"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
