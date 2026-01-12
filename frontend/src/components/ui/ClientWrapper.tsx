'use client';

import React from 'react';
import ErrorBoundary from './ErrorBoundary';

interface ClientWrapperProps {
  children: React.ReactNode;
}

export default function ClientWrapper({ children }: ClientWrapperProps) {
  return <ErrorBoundary>{children}</ErrorBoundary>;
}