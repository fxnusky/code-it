'use client';
import { useAuth } from '../contexts/auth_context'; 
import { GoogleOAuthProvider, GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
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
  console.log(GOOGLE_CLIENT_ID)
  const { login } = useAuth();
  const router = useRouter();

  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    try {
      const response = await AuthService.authenticateUser({ credentialResponse });
      if (response?.status === "success") {
        login(credentialResponse.credential || '');
        router.push(redirectTo); 
      } else {
        console.error('Authentication failed:', response?.detail);
      }
    } catch (error) {
      console.error('Authentication failed:', error);
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
    </GoogleOAuthProvider>
  );
};