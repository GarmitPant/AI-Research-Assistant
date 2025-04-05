from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from typing import List
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

router = APIRouter()

class EmailRequest(BaseModel):
    to: List[EmailStr]
    subject: str = "Response to your request"
    content: str

class EmailResponse(BaseModel):
    message: str

@router.post("/email", response_model=EmailResponse)
async def send_email(request: EmailRequest, req: Request):
    """
    Send an email using Gmail API
    """
    try:
        # Check if credentials are in the session
        if not req.session.get("credentials"):
            raise HTTPException(
                status_code=401,
                detail="Not authenticated with Gmail. Please login first."
            )
        
        # Get credentials from the session
        credentials_json = req.session.get("credentials")
        credentials = Credentials.from_authorized_user_info(
            json.loads(credentials_json)
        )
        
        # Check if credentials are valid and refresh if needed
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Update the session with refreshed credentials
            req.session["credentials"] = credentials.to_json()
        elif credentials.expired:
            raise HTTPException(
                status_code=401,
                detail="Gmail credentials expired. Please login again."
            )
        
        # Create Gmail API service
        service = build('gmail', 'v1', credentials=credentials)
        
        # Create a multipart message
        message = MIMEMultipart()
        message['to'] = ", ".join(request.to)
        message['subject'] = request.subject
        
        # Add HTML body
        html_content = f"""
        <html>
            <body>
                {request.content}
            </body>
        </html>
        """
        message.attach(MIMEText(html_content, 'html'))
        
        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Create the email request
        create_message = {
            'raw': encoded_message
        }
        
        # Send the email
        send_message = service.users().messages().send(
            userId="me", 
            body=create_message
        ).execute()
        
        return EmailResponse(message=f"Email sent successfully. Message ID: {send_message['id']}")
    
    except HttpError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Gmail API error: {error}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending email: {str(e)}"
        )
