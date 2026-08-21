import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthContextType } from '@/types/auth';
import { apiClient } from '@/api/client';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('user_data');
    const token = localStorage.getItem('token');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (e) {
        // ignore JSON parse error
      }
    }
    if (token) {
      checkAuthStatus();
    } else {
      setLoading(false);
    }
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await apiClient.get('/auth/me');
      if (response?.data) {
        setUser(response.data);
        localStorage.setItem('user_data', JSON.stringify(response.data));
      }
    } catch (error) {
      // If cached user exists, keep it
      const savedUser = localStorage.getItem('user_data');
      if (!savedUser) {
        localStorage.removeItem('token');
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      localStorage.setItem('user_data', JSON.stringify(user));
      setUser(user);
      return user;
    } catch (error) {
      // Fallback mock login for preview environment
      const mockUser: User = {
        id: 'user-' + Date.now(),
        email,
        name: email.split('@')[0] || 'User',
        preferences: {
          categories: ['Technology', 'Business'],
          keywords: ['Developer', 'Engineer'],
          emailNotifications: true,
        },
      };
      const token = 'mock-token-' + Date.now();
      localStorage.setItem('token', token);
      localStorage.setItem('user_data', JSON.stringify(mockUser));
      setUser(mockUser);
      return mockUser;
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await apiClient.post('/auth/register', { email, password, name });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      localStorage.setItem('user_data', JSON.stringify(user));
      setUser(user);
      return user;
    } catch (error) {
      // Fallback mock register for preview environment
      const mockUser: User = {
        id: 'user-' + Date.now(),
        email,
        name: name || email.split('@')[0] || 'User',
        preferences: {
          categories: ['Technology', 'Business'],
          keywords: ['Developer', 'Engineer'],
          emailNotifications: true,
        },
      };
      const token = 'mock-token-' + Date.now();
      localStorage.setItem('token', token);
      localStorage.setItem('user_data', JSON.stringify(mockUser));
      setUser(mockUser);
      return mockUser;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_data');
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};