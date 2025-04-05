from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

router = APIRouter()

# Define OAuth2 scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',  # For sending emails
    'https://www.googleapis.com/auth/gmail.readonly',  # For reading profile and emails
    'https://www.googleapis.com/auth/userinfo.email'  # For accessing user email address
]

# Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
def create_flow(redirect_uri: str):
    client_config = {
        "web": {
            "client_id": os.getenv("GMAIL_CLIENT_ID"),
            "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri]
        }
    }
    
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=SCOPES
    )
    flow.redirect_uri = redirect_uri
    return flow

class AuthStatus(BaseModel):
    authenticated: bool
    email: Optional[str] = None

@router.get("/status", response_model=AuthStatus)
async def auth_status(request: Request):
    """
    Check if the user is authenticated with Gmail
    """
    try:
        # Print session for debugging
        # print(f"Session in status: {dict(request.session)}")
        # Check if credentials are in the session
        credentials_json = request.session.get("credentials")
        # print(f"Credentials JSON: {credentials_json}")

        if credentials_json:
                credentials = Credentials.from_authorized_user_info(
                    json.loads(credentials_json)
                )
                
                
                # Check if credentials are valid
                if credentials and not credentials.expired:
                        # Get user email
                        service = build('gmail', 'v1', credentials=credentials)
                        
                        profile = service.users().getProfile(userId='me').execute()
                        print(f"Profile: {profile}")
                        email = profile.get('emailAddress')
                        
                        return AuthStatus(authenticated=True, email=email)
        
        return AuthStatus(authenticated=False)
    
    except Exception as e:
        return AuthStatus(authenticated=False)

@router.get("/login")
async def login(request: Request):
    """
    Initiate the OAuth2 flow for Gmail
    """
    try:
        # Create the flow
        redirect_uri = f"{os.getenv('API_BASE_URL', 'http://localhost:8000')}/api/auth/callback"
        flow = create_flow(redirect_uri)
        
        # Generate the authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        print(f"Login initiated with state: {state}")
        
        # Store the state in the session
        request.session["state"] = state
        
        print(f"Session after setting state: {dict(request.session)}")
        
        # Redirect to the authorization URL
        response = RedirectResponse(authorization_url)
        return response
    
    except Exception as e:
        print(f"Error in login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error initiating OAuth flow: {str(e)}"
        )

@router.get("/callback")
async def callback(request: Request, code: str, state: Optional[str] = None):
    """
    Handle the OAuth2 callback from Gmail
    """
    try:
        print(f"Callback received with state: {state}")
        print(f"Session in callback: {request.session}")
        
        # Verify state
        session_state = request.session.get("state")
        print(f"Session state from session: {session_state}")
        
        # If state verification fails but we have a code, we'll proceed anyway in development
        # In production, you would want to keep this strict
        if not state or (session_state and session_state != state):
            print(f"State mismatch: received={state}, session={session_state}")
            # For development, we'll continue anyway if we have a code
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise HTTPException(
                    status_code=400,
                    detail="Invalid state parameter"
                )
            else:
                print("Continuing despite state mismatch (development mode)")
        
        # Create the flow
        redirect_uri = f"{os.getenv('API_BASE_URL', 'http://localhost:8000')}/api/auth/callback"
        flow = create_flow(redirect_uri)
        
        # Exchange the authorization code for credentials
        try:
            flow.fetch_token(code=code)
        except Exception as token_error:
            # Check if the error is about scope changes
            if "Scope has changed" in str(token_error):
                print("Handling scope change by adding openid scope...")
                # Add openid to our scopes if not already there
                if 'openid' not in SCOPES:
                    SCOPES.append('openid')
                    print(f"Updated scopes: {SCOPES}")
                
                # Create a new flow with updated scopes
                flow = create_flow(redirect_uri)
                # Try fetching token again
                flow.fetch_token(code=code)
            else:
                # If it's another error, re-raise it
                raise
        
        credentials = flow.credentials
        
        # Store the credentials in the session
        request.session["credentials"] = credentials.to_json()
        
        print(f"Credentials stored in session: {credentials.to_json()[:100]}...")
        
        # Redirect to the frontend
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        return RedirectResponse(f"{frontend_url}/auth-success")
    
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error completing OAuth flow: {str(e)}"
        )

@router.get("/logout")
async def logout(request: Request):
    """
    Log out the user by removing the credentials from the session
    """
    try:
        # Print session contents for debugging
        print(f"Session before logout: {dict(request.session)}")
        
        # Remove credentials from the session
        if "credentials" in request.session:
            print("Removing credentials from session")
            del request.session["credentials"]
        else:
            print("No credentials found in session")
        
        # Print session after removal
        print(f"Session after logout: {dict(request.session)}")
        
        # Return success response
        return {"message": "Logged out successfully"}
    
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error logging out: {str(e)}"
        )
