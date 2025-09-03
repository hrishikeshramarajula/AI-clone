import React, { useState, useEffect, useCallback } from 'react';
import { useChatStore } from '@/store/chatStore';
import { useFileStore } from '@/store/fileStore';
import { useWebSocket } from '@/hooks/useWebSocket';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { Message, FileAttachment, ToolCall } from '@/types';
import { apiService } from '@/services/api';
import { cn } from '@/lib/utils';
import toast from 'react-hot-toast';

interface ChatInterfaceProps {
  className?: string;
}

export function ChatInterface({ className }: ChatInterfaceProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  
  const {
    conversations,
    currentConversationId,
    addMessage,
    updateMessage,
    deleteMessage,
    setStreaming,
    setTypingIndicator,
    getCurrentConversation,
    addConversation,
    addToolCall,
    updateToolCall,
  } = useChatStore();
  
  const { uploadedFiles } = useFileStore();
  const { isConnected, subscribe } = useWebSocket();
  
  const currentConversation = getCurrentConversation();
  const messages = currentConversation?.messages || [];
  
  useEffect(() => {
    if (!currentConversationId && conversations.length === 0) {
      const newConversation = {
        id: `conv_${Date.now()}`,
        title: 'New Chat',
        messages: [],
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      addConversation(newConversation);
    }
  }, [currentConversationId, conversations, addConversation]);
  
  useEffect(() => {
    const unsubscribeOutput = subscribe('command_output', (data) => {
      console.log('Command output:', data);
    });
    
    const unsubscribeToolCall = subscribe('tool_call', (data) => {
      if (currentConversationId && streamingMessage) {
        const toolCall: ToolCall = {
          id: `tool_${Date.now()}`,
          name: data.name,
          description: data.description,
          status: data.status,
          result: data.result,
          timestamp: new Date(),
        };
        
        const lastMessage = messages[messages.length - 1];
        if (lastMessage && lastMessage.role === 'assistant') {
          addToolCall(currentConversationId, lastMessage.id, toolCall);
        }
      }
    });
    
    return () => {
      unsubscribeOutput();
      unsubscribeToolCall();
    };
  }, [subscribe, currentConversationId, messages, streamingMessage, addToolCall]);
  
  const handleSendMessage = async (content: string, attachments?: FileAttachment[]) => {
    if (!currentConversationId) return;
    
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
      attachments,
      status: 'sent',
    };
    
    addMessage(currentConversationId, userMessage);
    setIsLoading(true);
    setTypingIndicator(true);
    
    try {
      const assistantMessageId = `msg_${Date.now() + 1}`;
      const assistantMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        status: 'streaming',
      };
      
      addMessage(currentConversationId, assistantMessage);
      setStreaming(true);
      
      await apiService.streamChat(
        currentConversationId,
        content,
        (chunk) => {
          setStreamingMessage((prev) => prev + chunk);
          updateMessage(currentConversationId, assistantMessageId, {
            content: streamingMessage + chunk,
          });
        },
        () => {
          updateMessage(currentConversationId, assistantMessageId, {
            status: 'sent',
          });
          setStreamingMessage('');
          setStreaming(false);
          setTypingIndicator(false);
          setIsLoading(false);
        },
        (error) => {
          console.error('Stream error:', error);
          updateMessage(currentConversationId, assistantMessageId, {
            content: 'Sorry, an error occurred while processing your request.',
            status: 'error',
          });
          setStreamingMessage('');
          setStreaming(false);
          setTypingIndicator(false);
          setIsLoading(false);
          toast.error('Failed to get response');
        }
      );
    } catch (error) {
      console.error('Send message error:', error);
      setIsLoading(false);
      setTypingIndicator(false);
      toast.error('Failed to send message');
    }
  };
  
  const handleCancelMessage = () => {
    setIsLoading(false);
    setStreaming(false);
    setTypingIndicator(false);
    setStreamingMessage('');
  };
  
  const handleEditMessage = (messageId: string, content: string) => {
    if (currentConversationId) {
      updateMessage(currentConversationId, messageId, { content });
    }
  };
  
  const handleDeleteMessage = (messageId: string) => {
    if (currentConversationId) {
      deleteMessage(currentConversationId, messageId);
    }
  };
  
  const handleRegenerateMessage = async (messageId: string) => {
    if (!currentConversationId) return;
    
    const messageIndex = messages.findIndex((m) => m.id === messageId);
    if (messageIndex === -1 || messageIndex === 0) return;
    
    const previousMessage = messages[messageIndex - 1];
    if (previousMessage.role !== 'user') return;
    
    deleteMessage(currentConversationId, messageId);
    
    await handleSendMessage(previousMessage.content, previousMessage.attachments);
  };
  
  const handleRunCode = async (code: string, language: string) => {
    if (!isConnected) {
      toast.error('WebSocket not connected');
      return;
    }
    
    try {
      const result = await apiService.executeCommand(`echo "${code}" | ${language}`);
      toast.success('Code executed successfully');
      console.log('Code execution result:', result);
    } catch (error) {
      console.error('Code execution error:', error);
      toast.error('Failed to execute code');
    }
  };
  
  const handleSelectFollowUp = (followUp: string) => {
    handleSendMessage(followUp);
  };
  
  return (
    <div className={cn('flex flex-col h-full', className)}>
      <MessageList
        messages={messages}
        isLoading={isLoading}
        isTyping={useChatStore((state) => state.typingIndicator)}
        onEditMessage={handleEditMessage}
        onDeleteMessage={handleDeleteMessage}
        onRegenerateMessage={handleRegenerateMessage}
        onRunCode={handleRunCode}
        onSelectFollowUp={handleSelectFollowUp}
        className="flex-1"
      />
      
      <MessageInput
        onSendMessage={handleSendMessage}
        onCancelMessage={handleCancelMessage}
        isLoading={isLoading}
        disabled={!currentConversationId}
      />
    </div>
  );
}