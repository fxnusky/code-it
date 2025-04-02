"use client";
import { ProtectedButton } from '../../../components/protected_button';
import { useEffect, useState } from 'react';
import styles from '../page.module.css';
import { useAuth } from '../../../contexts/auth_context';
import { useRouter } from 'next/navigation';

export default function LoginPage() { 
  const [redirectTo, setRedirectTo] = useState<string>("/join-room");
  const { isAuthenticated, email, logout } = useAuth();
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
      <div className={styles.card}>
        <div className={styles.cardContent}>
          {isAuthenticated ? (
            <>
              <h1 className={styles.title}>Welcome back!</h1>
              <p className={styles.description}>
                You're already logged in with the Google account: <strong>{email}</strong>
              </p>
              <div className={styles.buttonContainer}>
                <button 
                  onClick={logout}
                  className={styles.primaryButton}
                >
                  Log out to switch accounts
                </button>
              </div>
              <div className={styles.buttonContainer}>
                <button 
                  onClick={() => router.push("/profile")}
                  className={styles.secondaryButton}
                >
                  Back to the application
                </button>
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
                />
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}