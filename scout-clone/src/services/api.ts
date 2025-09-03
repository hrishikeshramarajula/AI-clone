import axios, { AxiosInstance } from 'axios';
import { Message, FileAttachment, Conversation } from '@/types';

class ApiService {
  private api: AxiosInstance;
  
  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
    
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }
  
  async sendMessage(conversationId: string, message: Omit<Message, 'id' | 'timestamp'>) {
    const response = await this.api.post(`/conversations/${conversationId}/messages`, message);
    return response.data;
  }
  
  async createConversation(title: string, model?: string): Promise<Conversation> {
    const response = await this.api.post('/conversations', { title, model });
    return response.data;
  }
  
  async getConversations(): Promise<Conversation[]> {
    const response = await this.api.get('/conversations');
    return response.data;
  }
  
  async getConversation(id: string): Promise<Conversation> {
    const response = await this.api.get(`/conversations/${id}`);
    return response.data;
  }
  
  async deleteConversation(id: string): Promise<void> {
    await this.api.delete(`/conversations/${id}`);
  }
  
  async uploadFile(file: File, onProgress?: (progress: number) => void): Promise<FileAttachment> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await this.api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress?.(progress);
        }
      },
    });
    
    return response.data;
  }
  
  async downloadFile(fileId: string): Promise<Blob> {
    const response = await this.api.get(`/files/${fileId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  }
  
  async executeCommand(command: string): Promise<{ output: string; exitCode: number }> {
    const response = await this.api.post('/bash', { command });
    return response.data;
  }
  
  async getModels(): Promise<{ id: string; name: string; description: string }[]> {
    const response = await this.api.get('/models');
    return response.data;
  }
  
  async streamChat(
    conversationId: string,
    message: string,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: any) => void
  ) {
    try {
      const response = await fetch(`${this.api.defaults.baseURL}/conversations/${conversationId}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
        },
        body: JSON.stringify({ message }),
      });
      
      if (!response.ok) throw new Error('Stream failed');
      
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) throw new Error('No reader available');
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          onComplete();
          break;
        }
        
        const chunk = decoder.decode(value);
        onChunk(chunk);
      }
    } catch (error) {
      onError(error);
    }
  }
}

export const apiService = new ApiService();