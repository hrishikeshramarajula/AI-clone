import React, { useEffect, useState } from 'react';
import { Wifi, WifiOff, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useWebSocket } from '@/hooks/useWebSocket';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

export function ConnectionStatus() {
  const { isConnected } = useWebSocket();
  const [showReconnecting, setShowReconnecting] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  useEffect(() => {
    let timeout: NodeJS.Timeout;
    
    if (!isConnected) {
      timeout = setTimeout(() => {
        setShowReconnecting(true);
        setReconnectAttempts((prev) => prev + 1);
      }, 1000);
    } else {
      setShowReconnecting(false);
      setReconnectAttempts(0);
    }

    return () => clearTimeout(timeout);
  }, [isConnected]);

  const getStatusIcon = () => {
    if (isConnected) {
      return <Wifi className="h-4 w-4" />;
    }
    if (showReconnecting) {
      return <WifiOff className="h-4 w-4 animate-pulse" />;
    }
    return <AlertCircle className="h-4 w-4" />;
  };

  const getStatusText = () => {
    if (isConnected) {
      return 'Connected';
    }
    if (showReconnecting) {
      return `Reconnecting... (${reconnectAttempts})`;
    }
    return 'Disconnected';
  };

  const getStatusColor = () => {
    if (isConnected) {
      return 'text-green-500';
    }
    if (showReconnecting) {
      return 'text-yellow-500';
    }
    return 'text-red-500';
  };

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div
            className={cn(
              'flex items-center gap-2 rounded-md px-2 py-1 text-sm transition-colors',
              getStatusColor()
            )}
          >
            {getStatusIcon()}
            <span className="hidden sm:inline">{getStatusText()}</span>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>WebSocket {getStatusText()}</p>
          {!isConnected && (
            <p className="text-xs text-muted-foreground">
              Check your connection or refresh the page
            </p>
          )}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}