"use client";
import { ProtectedButton } from '../../../components/protected_button';
import { useEffect, useState } from 'react';
import styles from '../page.module.css';
import { useAuth } from '../../../contexts/auth_context';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button"
import { LoadingState } from '../../../components/loading_state';

export default function LoginPage() { 
  const [redirectTo, setRedirectTo] = useState<string>("/join-room");
  const { isAuthenticated, email, logout } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const redirectParam = params.get('redirectTo');
    if (redirectParam) {
      setRedirectTo(redirectParam);
    }
  }, []);



  return (
    <div className={styles.container}>
      {isLoading? (
        <LoadingState></LoadingState>
      ):(
        <div className={styles.card}>
        <div className={styles.cardContent}>
          {isAuthenticated ? (
            <>
              <h1 className={styles.title}>Welcome back!</h1>
              <p className={styles.description}>
                You&apos;re already logged in with the Google account: <strong>{email}</strong>
              </p>
              <div className={styles.buttonContainer}>
                <Button 
                  onClick={logout}
                >
                  Log out to switch accounts
                </Button>
              </div>
              <div className={styles.buttonContainer}>
                <Button 
                  variant="secondary"
                  onClick={() => router.push("/profile")}
                >
                  Back to the application
                </Button>
              </div>
            </>
          ) : (
            <>
              <h1 className={styles.title}>Welcome!</h1>
              <p className={styles.description}>
                Please sign in with Google to continue to your account
              </p>
              <div className={styles.buttonContainer}>
                <ProtectedButton 
                  redirectTo={redirectTo} 
                  setIsLoading={setIsLoading}
                />
              </div>
            </>
          )}
        </div>
      </div>
      )}
      
    </div>
  );
}