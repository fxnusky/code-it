'use client';
import { useAuth } from '../contexts/auth_context'; 
import { GoogleOAuthProvider, GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
import AuthService from '../services/auth.service';

const GOOGLE_CLIENT_ID = "195860473074-e880uq1l37obetripidmk7odc2kcb184.apps.googleusercontent.com"

type ProtectedButtonProps = {
  redirectTo: string;
};

export const ProtectedButton = ({
  redirectTo,
}: ProtectedButtonProps) => {
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
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={handleError}
      />
    </GoogleOAuthProvider>
  );
};