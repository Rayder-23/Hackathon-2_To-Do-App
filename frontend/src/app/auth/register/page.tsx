'use client';

import { useRouter } from 'next/navigation';
import RegisterForm from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  const router = useRouter();

  const handleRegisterSuccess = () => {
    // Redirect to dashboard on successful registration
    router.push('/dashboard');
  };

  const handleSwitchToLogin = () => {
    // Switch to login page
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-cyan-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="absolute inset-0 z-0 overflow-hidden">
        <div className="absolute -top-52 left-1/4 w-72 h-72 bg-gradient-to-r from-indigo-400 to-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-52 right-1/4 w-72 h-72 bg-gradient-to-r from-cyan-400 to-teal-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 overflow-hidden">
          <div className="px-8 py-10">
            <div className="text-center mb-8">
              <div className="mx-auto flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-indigo-500 to-cyan-600 mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                </svg>
              </div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                Create Account
              </h2>
              <p className="mt-2 text-gray-600">Join us today to get started</p>
            </div>

            <RegisterForm
              onRegisterSuccess={handleRegisterSuccess}
              onSwitchToLogin={handleSwitchToLogin}
            />

            <div className="mt-6 text-center text-sm text-gray-600">
              <p>
                Already have an account?{' '}
                <button
                  onClick={handleSwitchToLogin}
                  className="font-medium text-indigo-600 hover:text-indigo-500 hover:underline transition-colors duration-200"
                >
                  Sign in
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}