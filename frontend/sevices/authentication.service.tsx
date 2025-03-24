import React from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

const GOOGLE_CLIENT_ID = "195860473074-e880uq1l37obetripidmk7odc2kcb184.apps.googleusercontent.com"


interface LoginProps {
  onLoginSuccess: (user: any) => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  
  const handleSuccess = async (credentialResponse: any) => {
    console.log('Login Success:', credentialResponse);

    // Send the token to the backend for validation
    const response = await fetch('http://localhost:8000/api/validate-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token: credentialResponse.credential }),
    });

    const data = await response.json();
    if (data.success) {
      console.log('User authenticated:', data.user);
      // Store the token in localStorage
      localStorage.setItem('google_token', credentialResponse.credential);
      // Notify the parent component of successful login
      onLoginSuccess(data.user);
    } else {
      console.error('Token validation failed:', data.message);
    }
  };

  const handleError = () => {
    console.log('Login Failed');
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

export default Login;