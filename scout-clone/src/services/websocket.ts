import { WebSocketMessage } from '@/types';

class WebSocketService {
  private socket: WebSocket | null = null;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private pingInterval: NodeJS.Timeout | null = null;
  private messageQueue: { event: string; data: any }[] = [];
  
  connect(url?: string) {
    const wsUrl = url || import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
    
    if (this.socket?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }
    
    try {
      this.socket = new WebSocket(wsUrl);
      
      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.emit('connected', { timestamp: new Date() });
        
        // Process queued messages
        while (this.messageQueue.length > 0) {
          const msg = this.messageQueue.shift();
          if (msg) {
            this.send(msg.event, msg.data);
          }
        }
        
        // Start ping interval to keep connection alive
        this.startPingInterval();
      };
      
      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        this.emit('disconnected', { code: event.code, reason: event.reason, timestamp: new Date() });
        this.stopPingInterval();
        
        // Attempt to reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.scheduleReconnect();
        }
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', { error, timestamp: new Date() });
      };
      
      this.socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      this.emit('error', { error, timestamp: new Date() });
    }
  }
  
  private scheduleReconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, Math.min(this.reconnectAttempts - 1, 4));
    
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
    
    this.reconnectTimeout = setTimeout(() => {
      this.connect();
    }, delay);
  }
  
  private startPingInterval() {
    this.stopPingInterval();
    
    this.pingInterval = setInterval(() => {
      if (this.isConnected()) {
        this.send('ping', { timestamp: Date.now() });
      }
    }, 30000); // Ping every 30 seconds
  }
  
  private stopPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }
  
  disconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    
    this.stopPingInterval();
    this.reconnectAttempts = this.maxReconnectAttempts; // Prevent auto-reconnect
    
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    
    this.messageQueue = [];
  }
  
  send(event: string, data: any) {
    const message = {
      type: event,
      data,
      timestamp: new Date().toISOString()
    };
    
    if (!this.isConnected()) {
      console.warn('WebSocket not connected, queueing message');
      this.messageQueue.push({ event, data });
      return;
    }
    
    try {
      this.socket!.send(JSON.stringify(message));
    } catch (error) {
      console.error('Failed to send WebSocket message:', error);
      this.messageQueue.push({ event, data });
    }
  }
  
  executeCommand(command: string, sessionId?: string) {
    this.send('execute_command', { 
      command, 
      sessionId: sessionId || 'default'
    });
  }
  
  sendMessage(message: string, conversationId: string) {
    this.send('chat_message', {
      message,
      conversationId,
      timestamp: new Date().toISOString()
    });
  }
  
  uploadFile(file: File, sessionId?: string) {
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result?.toString().split(',')[1];
      this.send('upload_file', {
        name: file.name,
        type: file.type,
        size: file.size,
        data: base64,
        sessionId: sessionId || 'default',
      });
    };
    reader.readAsDataURL(file);
  }
  
  joinSession(sessionId: string) {
    this.send('join_session', { sessionId });
  }
  
  leaveSession(sessionId: string) {
    this.send('leave_session', { sessionId });
  }
  
  sendToolCall(toolName: string, args: any) {
    this.send('tool_call', {
      name: toolName,
      arguments: args,
      timestamp: new Date().toISOString()
    });
  }
  
  on(event: string, callback: (data: any) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)?.add(callback);
    
    // Return unsubscribe function
    return () => {
      this.listeners.get(event)?.delete(callback);
    };
  }
  
  off(event: string, callback?: (data: any) => void) {
    if (!callback) {
      this.listeners.delete(event);
    } else {
      this.listeners.get(event)?.delete(callback);
    }
  }
  
  private emit(event: string, data: any) {
    this.listeners.get(event)?.forEach((callback) => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in WebSocket listener for event "${event}":`, error);
      }
    });
  }
  
  private handleMessage(message: any) {
    // Handle different message types from the server
    const { type, data } = message;
    
    switch (type) {
      case 'connected':
        this.emit('connected', data);
        break;
      case 'chat_response':
        this.emit('chat_response', data);
        break;
      case 'chat_stream':
        this.emit('chat_stream', data);
        break;
      case 'command_output':
        this.emit('command_output', data);
        break;
      case 'command_complete':
        this.emit('command_complete', data);
        break;
      case 'file_uploaded':
        this.emit('file_uploaded', data);
        break;
      case 'file_change':
        this.emit('file_change', data);
        break;
      case 'task_update':
        this.emit('task_update', data);
        break;
      case 'tool_call':
        this.emit('tool_call', data);
        break;
      case 'error':
        this.emit('error', data);
        break;
      case 'pong':
        // Ignore pong messages (heartbeat)
        break;
      case 'echo':
        this.emit('echo', data);
        break;
      default:
        console.warn('Unknown message type:', type);
        this.emit(type, data);
    }
  }
  
  isConnected(): boolean {
    return this.socket?.readyState === WebSocket.OPEN;
  }
  
  getReadyState(): number {
    return this.socket?.readyState ?? WebSocket.CLOSED;
  }
  
  getSocket(): WebSocket | null {
    return this.socket;
  }
}

export const wsService = new WebSocketService();