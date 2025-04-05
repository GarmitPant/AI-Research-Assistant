import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Function to check authentication status that can be called from anywhere
  const checkAuthStatus = async () => {
    setIsLoading(true);
    try {
      console.log('Checking auth status...');
      const response = await axios.get('http://localhost:8000/api/auth/status', {
        withCredentials: true
      });
      
      console.log('Auth status response:', response.data);
      setIsAuthenticated(response.data.authenticated);
      setUserEmail(response.data.email);
      return response.data;
    } catch (error) {
      console.error('Error checking auth status:', error);
      setIsAuthenticated(false);
      setUserEmail(null);
      return { authenticated: false, email: null };
    } finally {
      setIsLoading(false);
    }
  };

  // Check authentication status on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const login = () => {
    // Redirect to the backend login route
    window.location.href = 'http://localhost:8000/api/auth/login';
  };

  const logout = async () => {
    try {
      console.log('Logging out...');
      const response = await axios.get('http://localhost:8000/api/auth/logout', {
        withCredentials: true
      });
      console.log('Logout response:', response.data);
      
      // Force clear the authentication state
      setIsAuthenticated(false);
      setUserEmail(null);
      
      // Verify the logout was successful
      const authStatus = await checkAuthStatus();
      console.log('Auth status after logout:', authStatus);
      
      // Optionally, you could reload the page to ensure a clean state
      // window.location.reload();
    } catch (error) {
      console.error('Error logging out:', error);
      // Still clear the state even if there was an error
      setIsAuthenticated(false);
      setUserEmail(null);
    }
  };

  return (
    <AuthContext.Provider value={{ 
      isAuthenticated, 
      userEmail, 
      isLoading, 
      login, 
      logout,
      refreshAuth: checkAuthStatus 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
