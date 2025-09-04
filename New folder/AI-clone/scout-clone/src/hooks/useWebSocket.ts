import { useEffect, useRef, useState } from 'react';
import { wsService } from '@/services/websocket';

export function useWebSocket(url?: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const listenersRef = useRef<(() => void)[]>([]);
  
  useEffect(() => {
    wsService.connect(url);
    
    const unsubscribeConnected = wsService.on('connected', () => {
      setIsConnected(true);
    });
    
    const unsubscribeDisconnected = wsService.on('disconnected', () => {
      setIsConnected(false);
    });
    
    listenersRef.current = [unsubscribeConnected, unsubscribeDisconnected];
    
    return () => {
      listenersRef.current.forEach((unsub) => unsub());
      wsService.disconnect();
    };
  }, [url]);
  
  const sendMessage = (event: string, data: any) => {
    wsService.send(event, data);
  };
  
  const subscribe = (event: string, callback: (data: any) => void) => {
    const unsubscribe = wsService.on(event, (data) => {
      setLastMessage({ event, data, timestamp: new Date() });
      callback(data);
    });
    
    listenersRef.current.push(unsubscribe);
    return unsubscribe;
  };
  
  return {
    isConnected,
    sendMessage,
    subscribe,
    lastMessage,
    wsService,
  };
}