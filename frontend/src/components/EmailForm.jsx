import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

// Create an axios instance with the base URL and credentials config
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
});

const EmailForm = ({ content }) => {
  const [recipients, setRecipients] = useState('');
  const [subject, setSubject] = useState('Research Response');
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState({ type: '', message: '' });
  const { isAuthenticated, userEmail, login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      setStatus({
        type: 'error',
        message: 'Please login with Google to send emails'
      });
      return;
    }
    
    if (!recipients.trim()) {
      setStatus({
        type: 'error',
        message: 'Please enter at least one recipient email address'
      });
      return;
    }

    setIsLoading(true);
    setStatus({ type: '', message: '' });

    try {
      // Split the recipients by comma and trim whitespace
      const recipientList = recipients
        .split(',')
        .map(email => email.trim())
        .filter(email => email);

      const response = await api.post('/api/email', {
        to: recipientList,
        subject,
        content
      });

      setStatus({
        type: 'success',
        message: 'Email sent successfully!'
      });
    } catch (err) {
      setStatus({
        type: 'error',
        message: err.response?.data?.detail || 'Failed to send email. Please try again.'
      });
      console.error('Error sending email:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {!isAuthenticated ? (
        <div className="bg-blue-50 p-4 rounded-md border border-blue-200 mb-4">
          <p className="text-blue-700 mb-2">You need to login with Google to send emails</p>
          <button
            onClick={login}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
          >
            Login with Google
          </button>
        </div>
      ) : (
        <div className="bg-green-50 p-4 rounded-md border border-green-200 mb-4">
          <p className="text-green-700">Logged in as: <strong>{userEmail}</strong></p>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="recipients" className="block text-sm font-medium text-gray-700 mb-1">
          Recipients
        </label>
        <input
          id="recipients"
          type="text"
          value={recipients}
          onChange={(e) => setRecipients(e.target.value)}
          placeholder="email@example.com, another@example.com"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <p className="text-xs text-gray-500 mt-1">
          Separate multiple email addresses with commas
        </p>
      </div>
      
      <div>
        <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-1">
          Subject
        </label>
        <input
          id="subject"
          type="text"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Email subject"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      
      <div className="bg-gray-50 p-3 rounded-md border border-gray-200">
        <p className="text-sm font-medium text-gray-700 mb-2">Content Preview:</p>
        <div 
          className="text-sm text-gray-600 max-h-32 overflow-y-auto p-2 bg-white rounded border border-gray-300"
          dangerouslySetInnerHTML={{ __html: content || '<em>No content to preview</em>' }}
        />
      </div>
      
      {status.message && (
        <div className={`p-3 rounded-md ${
          status.type === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : 
          'bg-red-50 text-red-700 border border-red-200'
        }`}>
          {status.message}
        </div>
      )}
      
      <div>
        <button
          type="submit"
          disabled={isLoading || !recipients.trim() || !content.trim()}
          className={`w-full py-2 px-4 rounded-md text-white font-medium ${
            isLoading || !recipients.trim() || !content.trim()
              ? 'bg-green-300 cursor-not-allowed' 
              : 'bg-green-600 hover:bg-green-700'
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Sending...
            </span>
          ) : (
            'Send Email'
          )}
        </button>
      </div>
    </form>
    </div>
  );
};

export default EmailForm;
