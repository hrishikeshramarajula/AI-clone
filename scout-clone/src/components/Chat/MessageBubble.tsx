import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { format } from 'date-fns';
import { motion } from 'framer-motion';
import { Message, ToolCall } from '@/types';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Copy, 
  Check, 
  Download, 
  RefreshCw, 
  Edit, 
  Trash2,
  ChevronDown,
  ChevronUp,
  Sparkles,
  User,
  Bot,
  Loader2,
  PlayCircle,
  CheckCircle,
  XCircle,
  Clock
} from 'lucide-react';
import { cn } from '@/lib/utils';
import toast from 'react-hot-toast';

interface MessageBubbleProps {
  message: Message;
  onEdit?: (messageId: string, content: string) => void;
  onDelete?: (messageId: string) => void;
  onRegenerate?: (messageId: string) => void;
  onRunCode?: (code: string, language: string) => void;
  onSelectFollowUp?: (followUp: string) => void;
}

export function MessageBubble({ 
  message, 
  onEdit, 
  onDelete, 
  onRegenerate,
  onRunCode,
  onSelectFollowUp
}: MessageBubbleProps) {
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(message.content);
  const [showToolCalls, setShowToolCalls] = useState(false);
  
  const handleCopyCode = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(id);
    toast.success('Code copied to clipboard');
    setTimeout(() => setCopiedCode(null), 2000);
  };
  
  const handleSaveEdit = () => {
    if (editContent.trim() && onEdit) {
      onEdit(message.id, editContent);
      setIsEditing(false);
    }
  };
  
  const getToolCallIcon = (status: ToolCall['status']) => {
    switch (status) {
      case 'pending':
        return <Clock className="h-3 w-3" />;
      case 'running':
        return <Loader2 className="h-3 w-3 animate-spin" />;
      case 'completed':
        return <CheckCircle className="h-3 w-3 text-green-500" />;
      case 'error':
        return <XCircle className="h-3 w-3 text-red-500" />;
    }
  };
  
  const isUser = message.role === 'user';
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        'group flex gap-3 px-4 py-6',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      {!isUser && (
        <Avatar className="h-8 w-8 mt-0.5">
          <AvatarFallback className="bg-primary/10">
            <Bot className="h-4 w-4" />
          </AvatarFallback>
        </Avatar>
      )}
      
      <div className={cn(
        'flex flex-col gap-2 max-w-[80%]',
        isUser && 'items-end'
      )}>
        <div className={cn(
          'relative rounded-lg px-4 py-3',
          isUser ? 'bg-primary text-primary-foreground' : 'bg-muted'
        )}>
          {message.status === 'streaming' && (
            <div className="absolute -top-1 -right-1">
              <Sparkles className="h-4 w-4 text-primary animate-pulse" />
            </div>
          )}
          
          {isEditing ? (
            <div className="space-y-2">
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full min-h-[100px] p-2 bg-background rounded resize-none"
                autoFocus
              />
              <div className="flex gap-2">
                <Button size="sm" onClick={handleSaveEdit}>Save</Button>
                <Button size="sm" variant="outline" onClick={() => setIsEditing(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    const codeId = `code_${message.id}_${Math.random()}`;
                    
                    return match ? (
                      <div className="relative group/code my-4">
                        <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover/code:opacity-100 transition-opacity">
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-7 px-2"
                            onClick={() => handleCopyCode(String(children), codeId)}
                          >
                            {copiedCode === codeId ? (
                              <Check className="h-3 w-3" />
                            ) : (
                              <Copy className="h-3 w-3" />
                            )}
                          </Button>
                          {onRunCode && (
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-7 px-2"
                              onClick={() => onRunCode(String(children), match[1])}
                            >
                              <PlayCircle className="h-3 w-3" />
                            </Button>
                          )}
                        </div>
                        <SyntaxHighlighter
                          style={oneDark as any}
                          language={match[1]}
                          PreTag="div"
                        >
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      </div>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}
          
          {message.attachments && message.attachments.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {message.attachments.map((attachment) => (
                <Card key={attachment.id} className="p-2 flex items-center gap-2">
                  <div className="text-xs">
                    <p className="font-medium">{attachment.name}</p>
                    <p className="text-muted-foreground">
                      {(attachment.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <Button size="sm" variant="ghost" className="h-6 w-6 p-0">
                    <Download className="h-3 w-3" />
                  </Button>
                </Card>
              ))}
            </div>
          )}
          
          {message.followUps && message.followUps.length > 0 && (
            <div className="mt-4 space-y-2">
              <p className="text-xs font-medium text-muted-foreground">Suggested follow-ups:</p>
              <div className="flex flex-wrap gap-2">
                {message.followUps.map((followUp) => (
                  <Button
                    key={followUp.id}
                    variant="outline"
                    size="sm"
                    className="justify-start"
                    onClick={() => onSelectFollowUp?.(followUp.prompt)}
                  >
                    <span className="mr-2">{followUp.emoji}</span>
                    {followUp.title}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </div>
        
        {message.toolCalls && message.toolCalls.length > 0 && (
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              className="h-6 text-xs text-muted-foreground"
              onClick={() => setShowToolCalls(!showToolCalls)}
            >
              {showToolCalls ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
              {message.toolCalls.length} tool call{message.toolCalls.length > 1 ? 's' : ''}
            </Button>
          </div>
        )}
        
        {showToolCalls && message.toolCalls && (
          <div className="space-y-1">
            {message.toolCalls.map((toolCall) => (
              <div key={toolCall.id} className="flex items-center gap-2 text-xs">
                {getToolCallIcon(toolCall.status)}
                <span className="font-medium">{toolCall.name}</span>
                <span className="text-muted-foreground">{toolCall.description}</span>
              </div>
            ))}
          </div>
        )}
        
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span>{format(new Date(message.timestamp), 'HH:mm')}</span>
          {message.metadata?.model && (
            <Badge variant="secondary" className="text-xs">
              {message.metadata.model}
            </Badge>
          )}
          {message.metadata?.tokensUsed && (
            <span>{message.metadata.tokensUsed} tokens</span>
          )}
          
          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity ml-auto">
            {!isUser && onRegenerate && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={() => onRegenerate(message.id)}
              >
                <RefreshCw className="h-3 w-3" />
              </Button>
            )}
            {onEdit && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={() => setIsEditing(true)}
              >
                <Edit className="h-3 w-3" />
              </Button>
            )}
            {onDelete && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={() => onDelete(message.id)}
              >
                <Trash2 className="h-3 w-3" />
              </Button>
            )}
          </div>
        </div>
      </div>
      
      {isUser && (
        <Avatar className="h-8 w-8 mt-0.5">
          <AvatarFallback>
            <User className="h-4 w-4" />
          </AvatarFallback>
        </Avatar>
      )}
    </motion.div>
  );
}