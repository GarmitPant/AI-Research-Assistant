import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PromptForm from './components/PromptForm';
import ResponseEditor from './components/ResponseEditor';
import EmailForm from './components/EmailForm';
import AuthSuccess from './components/AuthSuccess';
import UserMenu from './components/UserMenu';
import { AuthProvider } from './context/AuthContext';
import axios from 'axios';

// Create an axios instance with the base URL and credentials config
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
});

const MainContent = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [responseContent, setResponseContent] = useState('');
  const [error, setError] = useState('');

  const handlePromptSubmit = async (prompt, content) => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await api.post('/api/groq', {
        prompt,
        content
      });
      
      setResponseContent(response.data.output);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while processing your request');
      console.error('Error processing prompt:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <header className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-gray-800">AI Research Assistant</h1>
          <UserMenu />
        </div>
        <p className="text-gray-600 text-center">Research, generate responses, and send emails</p>
      </header>

      <main className="space-y-8">
        <section className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Research Query</h2>
          <PromptForm onSubmit={handlePromptSubmit} isLoading={isLoading} />
        </section>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        <section className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Generated Response</h2>
          <ResponseEditor 
            content={responseContent} 
            onChange={setResponseContent} 
          />
        </section>

        <section className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Send Response via Email</h2>
          <EmailForm content={responseContent} />
        </section>
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© 2025 AI Research Assistant</p>
      </footer>
    </div>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainContent />} />
          <Route path="/auth-success" element={<AuthSuccess />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;