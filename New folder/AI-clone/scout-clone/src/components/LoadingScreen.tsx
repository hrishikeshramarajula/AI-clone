import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingScreenProps {
  message?: string;
}

export function LoadingScreen({ message = 'Loading Scout AI...' }: LoadingScreenProps) {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-background">
      <div className="flex flex-col items-center space-y-4">
        <div className="relative">
          <div className="h-16 w-16 rounded-full border-4 border-primary/20" />
          <Loader2 className="absolute inset-0 h-16 w-16 animate-spin text-primary" />
        </div>
        <div className="text-center">
          <p className="text-lg font-semibold">{message}</p>
          <p className="text-sm text-muted-foreground">Please wait while we set things up</p>
        </div>
      </div>
    </div>
  );
}