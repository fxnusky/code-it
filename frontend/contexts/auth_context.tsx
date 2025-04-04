'use client';
import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { setCookie, deleteCookie, getCookie } from 'cookies-next';
import { jwtDecode } from 'jwt-decode';

type AuthContextType = {
  token: string;
  email: string | null;
  isAuthenticated: boolean;
  isInitialized: boolean;
  login: (token: string) => void; 
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string>('');
  const [email, setEmail] = useState<string | null>(null); 
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const storedToken = getCookie('token');
    const storedEmail = getCookie('email'); 
    
    if (storedToken && typeof storedToken === 'string') {
      setToken(storedToken);
      if (storedEmail && typeof storedEmail === 'string') {
        setEmail(storedEmail);
      }
    }
    setIsInitialized(true);
  }, []);

  const login = (newToken: string) => {
    const decoded = jwtDecode(newToken) as { email: string };
    
    setToken(newToken);
    setEmail(decoded.email);
    setCookie('token', newToken, {
      maxAge: 60 * 60 * 24 * 7,
      secure: true,
      sameSite: 'lax',
    });
    setCookie('email', decoded.email, {
      maxAge: 60 * 60 * 24 * 7,
      secure: true,
      sameSite: 'lax',
    });
  };

  const logout = () => {
    setToken('');
    setEmail(null);
    deleteCookie('token');
    deleteCookie('email');
  };

  const value = {
    token,
    email,
    isAuthenticated: !!token,
    isInitialized,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};