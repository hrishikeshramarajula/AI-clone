export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  attachments?: FileAttachment[];
  codeBlocks?: CodeBlock[];
  status?: 'sending' | 'sent' | 'error' | 'streaming';
  metadata?: {
    model?: string;
    tokensUsed?: number;
    executionTime?: number;
  };
  followUps?: FollowUp[];
  toolCalls?: ToolCall[];
}

export interface ToolCall {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  result?: any;
  timestamp: Date;
}

export interface FollowUp {
  id: string;
  emoji: string;
  title: string;
  prompt: string;
}

export interface FileAttachment {
  id: string;
  name: string;
  size: number;
  type: string;
  url: string;
  preview?: string;
  uploadProgress?: number;
  status: 'uploading' | 'uploaded' | 'error';
}

export interface CodeBlock {
  id: string;
  language: string;
  code: string;
  filename?: string;
  lineNumbers?: boolean;
  executable?: boolean;
  output?: string;
  status?: 'idle' | 'running' | 'success' | 'error';
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  model?: string;
  pinned?: boolean;
  archived?: boolean;
}

export interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  progress?: number;
  description?: string;
  createdAt: Date;
  completedAt?: Date;
}

export interface WebSocketMessage {
  type: 'command' | 'output' | 'error' | 'status' | 'complete';
  data: any;
  timestamp: Date;
}

export interface Settings {
  theme: 'light' | 'dark' | 'system';
  model: string;
  temperature?: number;
  maxTokens?: number;
  streamResponse: boolean;
  showTokenUsage: boolean;
  autoSave: boolean;
  keyboardShortcuts: boolean;
  fontSize: 'small' | 'medium' | 'large';
  codeTheme: string;
}

export interface ProjectFile {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'directory';
  size?: number;
  modified?: Date;
  children?: ProjectFile[];
  content?: string;
  language?: string;
}