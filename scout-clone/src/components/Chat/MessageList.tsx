import React, { useEffect, useRef } from 'react';
import { Virtuoso } from 'react-virtuoso';
import { AnimatePresence, motion } from 'framer-motion';
import { Message } from '@/types';
import { MessageBubble } from './MessageBubble';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
  isTyping?: boolean;
  onEditMessage?: (messageId: string, content: string) => void;
  onDeleteMessage?: (messageId: string) => void;
  onRegenerateMessage?: (messageId: string) => void;
  onRunCode?: (code: string, language: string) => void;
  onSelectFollowUp?: (followUp: string) => void;
  className?: string;
}

export function MessageList({
  messages,
  isLoading,
  isTyping,
  onEditMessage,
  onDeleteMessage,
  onRegenerateMessage,
  onRunCode,
  onSelectFollowUp,
  className,
}: MessageListProps) {
  const virtuosoRef = useRef<any>(null);
  
  useEffect(() => {
    if (virtuosoRef.current) {
      virtuosoRef.current.scrollToIndex({
        index: messages.length - 1,
        behavior: 'smooth',
      });
    }
  }, [messages.length]);
  
  const EmptyState = () => (
    <div className="flex flex-col items-center justify-center h-full text-center p-8">
      <div className="max-w-md space-y-4">
        <h2 className="text-2xl font-semibold">Start a conversation</h2>
        <p className="text-muted-foreground">
          Ask me anything! I can help with coding, research, analysis, and much more.
        </p>
        <div className="grid grid-cols-2 gap-3 mt-6">
          <button
            onClick={() => onSelectFollowUp?.("Help me write a Python script")}
            className="p-3 text-left border rounded-lg hover:bg-muted transition-colors"
          >
            <span className="text-sm font-medium">💻 Code Assistant</span>
            <p className="text-xs text-muted-foreground mt-1">
              Write and debug code
            </p>
          </button>
          <button
            onClick={() => onSelectFollowUp?.("Research the latest AI developments")}
            className="p-3 text-left border rounded-lg hover:bg-muted transition-colors"
          >
            <span className="text-sm font-medium">🔬 Research</span>
            <p className="text-xs text-muted-foreground mt-1">
              Analyze and explore topics
            </p>
          </button>
          <button
            onClick={() => onSelectFollowUp?.("Help me with data analysis")}
            className="p-3 text-left border rounded-lg hover:bg-muted transition-colors"
          >
            <span className="text-sm font-medium">📊 Data Analysis</span>
            <p className="text-xs text-muted-foreground mt-1">
              Process and visualize data
            </p>
          </button>
          <button
            onClick={() => onSelectFollowUp?.("Create a website mockup")}
            className="p-3 text-left border rounded-lg hover:bg-muted transition-colors"
          >
            <span className="text-sm font-medium">🎨 Design</span>
            <p className="text-xs text-muted-foreground mt-1">
              Create mockups and designs
            </p>
          </button>
        </div>
      </div>
    </div>
  );
  
  if (messages.length === 0 && !isLoading) {
    return <EmptyState />;
  }
  
  return (
    <div className={cn('flex-1 overflow-hidden', className)}>
      <Virtuoso
        ref={virtuosoRef}
        data={messages}
        itemContent={(index, message) => (
          <MessageBubble
            key={message.id}
            message={message}
            onEdit={onEditMessage}
            onDelete={onDeleteMessage}
            onRegenerate={onRegenerateMessage}
            onRunCode={onRunCode}
            onSelectFollowUp={onSelectFollowUp}
          />
        )}
        followOutput="smooth"
        alignToBottom
        className="h-full"
      />
      
      <AnimatePresence>
        {(isLoading || isTyping) && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="flex items-center gap-2 px-4 py-3 text-muted-foreground"
          >
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-sm">
              {isTyping ? 'Scout is typing...' : 'Processing...'}
            </span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}