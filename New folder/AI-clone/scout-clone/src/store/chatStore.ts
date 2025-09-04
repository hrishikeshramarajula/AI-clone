import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Message, Conversation, FollowUp, ToolCall } from '@/types';

interface ChatState {
  conversations: Conversation[];
  currentConversationId: string | null;
  isStreaming: boolean;
  typingIndicator: boolean;
  
  addConversation: (conversation: Conversation) => void;
  deleteConversation: (id: string) => void;
  setCurrentConversation: (id: string) => void;
  updateConversationTitle: (id: string, title: string) => void;
  pinConversation: (id: string) => void;
  unpinConversation: (id: string) => void;
  archiveConversation: (id: string) => void;
  unarchiveConversation: (id: string) => void;
  
  addMessage: (conversationId: string, message: Message) => void;
  updateMessage: (conversationId: string, messageId: string, updates: Partial<Message>) => void;
  deleteMessage: (conversationId: string, messageId: string) => void;
  
  setStreaming: (streaming: boolean) => void;
  setTypingIndicator: (typing: boolean) => void;
  
  addToolCall: (conversationId: string, messageId: string, toolCall: ToolCall) => void;
  updateToolCall: (conversationId: string, messageId: string, toolCallId: string, updates: Partial<ToolCall>) => void;
  
  clearConversations: () => void;
  getCurrentConversation: () => Conversation | null;
  getPinnedConversations: () => Conversation[];
  getArchivedConversations: () => Conversation[];
  getActiveConversations: () => Conversation[];
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      conversations: [],
      currentConversationId: null,
      isStreaming: false,
      typingIndicator: false,
      
      addConversation: (conversation) => {
        set((state) => ({
          conversations: [...state.conversations, conversation],
          currentConversationId: conversation.id,
        }));
      },
      
      deleteConversation: (id) => {
        set((state) => ({
          conversations: state.conversations.filter((c) => c.id !== id),
          currentConversationId: state.currentConversationId === id ? null : state.currentConversationId,
        }));
      },
      
      setCurrentConversation: (id) => {
        set({ currentConversationId: id });
      },
      
      updateConversationTitle: (id, title) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === id ? { ...conv, title, updatedAt: new Date() } : conv
          ),
        }));
      },
      
      pinConversation: (id) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === id ? { ...conv, pinned: true, updatedAt: new Date() } : conv
          ),
        }));
      },
      
      unpinConversation: (id) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === id ? { ...conv, pinned: false, updatedAt: new Date() } : conv
          ),
        }));
      },
      
      archiveConversation: (id) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === id ? { ...conv, archived: true, updatedAt: new Date() } : conv
          ),
        }));
      },
      
      unarchiveConversation: (id) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === id ? { ...conv, archived: false, updatedAt: new Date() } : conv
          ),
        }));
      },
      
      addMessage: (conversationId, message) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === conversationId
              ? { ...conv, messages: [...conv.messages, message], updatedAt: new Date() }
              : conv
          ),
        }));
      },
      
      updateMessage: (conversationId, messageId, updates) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === conversationId
              ? {
                  ...conv,
                  messages: conv.messages.map((msg) =>
                    msg.id === messageId ? { ...msg, ...updates } : msg
                  ),
                }
              : conv
          ),
        }));
      },
      
      deleteMessage: (conversationId, messageId) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === conversationId
              ? {
                  ...conv,
                  messages: conv.messages.filter((msg) => msg.id !== messageId),
                }
              : conv
          ),
        }));
      },
      
      setStreaming: (streaming) => {
        set({ isStreaming: streaming });
      },
      
      setTypingIndicator: (typing) => {
        set({ typingIndicator: typing });
      },
      
      addToolCall: (conversationId, messageId, toolCall) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === conversationId
              ? {
                  ...conv,
                  messages: conv.messages.map((msg) =>
                    msg.id === messageId
                      ? { ...msg, toolCalls: [...(msg.toolCalls || []), toolCall] }
                      : msg
                  ),
                }
              : conv
          ),
        }));
      },
      
      updateToolCall: (conversationId, messageId, toolCallId, updates) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === conversationId
              ? {
                  ...conv,
                  messages: conv.messages.map((msg) =>
                    msg.id === messageId
                      ? {
                          ...msg,
                          toolCalls: msg.toolCalls?.map((tc) =>
                            tc.id === toolCallId ? { ...tc, ...updates } : tc
                          ),
                        }
                      : msg
                  ),
                }
              : conv
          ),
        }));
      },
      
      clearConversations: () => {
        set({ conversations: [], currentConversationId: null });
      },
      
      getCurrentConversation: () => {
        const state = get();
        return state.conversations.find((c) => c.id === state.currentConversationId) || null;
      },
      
      getPinnedConversations: () => {
        const state = get();
        return state.conversations.filter((c) => c.pinned && !c.archived);
      },
      
      getArchivedConversations: () => {
        const state = get();
        return state.conversations.filter((c) => c.archived);
      },
      
      getActiveConversations: () => {
        const state = get();
        return state.conversations.filter((c) => !c.archived);
      },
    }),
    {
      name: 'scout-chat-storage',
    }
  )
);