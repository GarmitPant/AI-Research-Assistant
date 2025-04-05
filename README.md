# AI Research Assistant

A full-stack application that helps users research topics, generate responses, and send emails using AI technology.

## Features

- **AI-Powered Research**: Ask research questions and get comprehensive answers
- **Gmail Integration**: Send emails directly from the application
- **OAuth Authentication**: Secure login with Gmail
- **Rich Text Editing**: Format your responses before sending

## Tech Stack

### Frontend
- React with Vite
- React Router for navigation
- TailwindCSS for styling
- Axios for API requests
- React Quill for rich text editing

### Backend
- FastAPI for the REST API
- Google OAuth for authentication
- Gmail API for sending emails
- Groq API for AI-powered responses

## Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- Google Cloud Platform account with Gmail API enabled
- Groq API key

## Environment Variables

### Backend (.env)
```
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
GROQ_API_KEY=your_groq_api_key
SESSION_SECRET_KEY=a_secure_random_string
```

## Installation

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the required environment variables

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API and OAuth consent screen
4. Configure the OAuth consent screen with the following scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/userinfo.email`
   - `openid`
5. Create OAuth credentials (Web application type)
6. Add authorized redirect URIs:
   - `http://localhost:8000/api/auth/callback`
7. Add authorized JavaScript origins:
   - `http://localhost:5173`

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Log in with your Gmail account
3. Enter a research question in the prompt field
4. Review and edit the generated response
5. Send the response via email

## Project Structure

```
ai-research-assistant/
├── backend/
│   ├── routes/
│   │   ├── auth.py       # Authentication routes
│   │   ├── email.py      # Email sending functionality
│   │   ├── groq.py       # AI model integration
│   │   ├── scrape.py     # Web scraping functionality
│   │   └── search.py     # Search functionality
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/   # React components
    │   ├── context/      # React context providers
    │   ├── App.jsx       # Main application component
    │   └── main.jsx      # Entry point
    ├── package.json      # Node.js dependencies
    └── index.html        # HTML template
```

## License

MIT

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Groq](https://groq.com/)
- [Google APIs](https://developers.google.com/apis-explorer)
