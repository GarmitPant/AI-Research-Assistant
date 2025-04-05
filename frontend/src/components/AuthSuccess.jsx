import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AuthSuccess = () => {
  const { refreshAuth } = useAuth();
  const navigate = useNavigate();
  const [message, setMessage] = useState('Completing authentication...');

  useEffect(() => {
    const completeAuth = async () => {
      try {
        // Refresh the auth status to update the context
        const authResult = await refreshAuth();
        
        if (authResult.authenticated) {
          setMessage(`Authentication successful! Logged in as ${authResult.email}`);
          // Redirect to home page after a short delay
          setTimeout(() => {
            navigate('/');
          }, 2000);
        } else {
          setMessage('Authentication failed. Please try again.');
        }
      } catch (error) {
        console.error('Error completing authentication:', error);
        setMessage('An error occurred during authentication.');
      }
    };

    completeAuth();
  }, [refreshAuth, navigate]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
        <h1 className="text-2xl font-bold mb-4">Authentication</h1>
        <p className="text-gray-700">{message}</p>
        {message.includes('successful') && (
          <div className="mt-4 text-green-600">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthSuccess;