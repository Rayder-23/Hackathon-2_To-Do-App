import React, { useEffect, useState } from 'react';
import { betterAuthService } from '@/services/auth-service';
import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = <div>Loading...</div>,
  redirectTo = '/login'
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const checkAuth = async () => {
      const authenticated = await betterAuthService.isAuthenticated();
      setIsAuthenticated(authenticated);

      if (!authenticated) {
        // Store the original path for redirect after login
        sessionStorage.setItem('redirectAfterLogin', pathname);
        router.push(redirectTo);
      }
    };

    checkAuth();
  }, [pathname, redirectTo, router]);

  if (isAuthenticated === null) {
    // Still checking authentication status
    return fallback;
  }

  if (!isAuthenticated) {
    // Redirect has already happened, return nothing
    return null;
  }

  // User is authenticated, render the children
  return <>{children}</>;
};

export default ProtectedRoute;