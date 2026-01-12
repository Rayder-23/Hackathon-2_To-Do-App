'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { betterAuthService } from '@/services/auth-service';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const checkAuthAndRedirect = async () => {
      const isAuthenticated = await betterAuthService.isAuthenticated();
      if (isAuthenticated) {
        router.push('/dashboard');
      } else {
        router.push('/auth/login');
      }
    };

    checkAuthAndRedirect();
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Redirecting...</p>
    </div>
  );
}
