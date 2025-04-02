// components/require_auth.tsx
'use client';
import { useAuth } from '../contexts/auth_context';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';

export const RequireAuth = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isInitialized } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (isInitialized && !isAuthenticated) {
      router.push(`/login?redirectTo=${encodeURIComponent(pathname || '/join-room')}`);
    }
  }, [isAuthenticated, isInitialized, router, pathname]);

  if (!isInitialized) {
    return null;
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
};