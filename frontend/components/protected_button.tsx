'use client';
import { useAuth } from '../contexts/auth_context'; 
import { GoogleOAuthProvider, GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import AuthService from '../services/auth.service';

const GOOGLE_CLIENT_ID = "921496431352-h75ism3ee3p8oiku1dmq2ndgaetluh2i.apps.googleusercontent.com"

type ProtectedButtonProps = {
  redirectTo: string;
  setIsLoading: (isLoading: boolean) => void;
};

export const ProtectedButton = ({
  redirectTo,
  setIsLoading
}: ProtectedButtonProps) => {
  const { login } = useAuth();
  const router = useRouter();
  const [errorMessage, setErrorMessage] = useState('')


  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    try {
      const response = await AuthService.authenticateUser({ credentialResponse });
      if (response?.status === "success") {
        setErrorMessage('')
        login(credentialResponse.credential || '');
        router.push(redirectTo); 
      } else {
        console.error('Authentication failed:', response?.detail);
        setErrorMessage('Authentication failed')
      }
    } catch (error) {
      console.error('Authentication failed:', error);
      setErrorMessage('Authentication failed')
    }
  };

  const handleError = () => {
    console.error('Google OAuth failed');
  };

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <div onClick={() => setIsLoading(true)}>
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={handleError}
        />
      </div>
      <div id='error_message'>{errorMessage}</div>
    </GoogleOAuthProvider>
  );
};