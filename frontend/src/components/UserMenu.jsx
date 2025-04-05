import React from 'react';
import { useAuth } from '../context/AuthContext';

const UserMenu = () => {
  const { isAuthenticated, userEmail, logout, login } = useAuth();

  return (
    <div className="flex items-center space-x-4">
      {isAuthenticated ? (
        <>
          <span className="text-sm text-gray-700">{userEmail}</span>
          <button
            onClick={logout}
            className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Logout
          </button>
        </>
      ) : (
        <button
          onClick={login}
          className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          Login with Gmail
        </button>
      )}
    </div>
  );
};

export default UserMenu;
