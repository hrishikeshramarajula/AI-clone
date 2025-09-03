import React, { useState, useRef, useCallback, KeyboardEvent } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { 
  Send, 
  Paperclip, 
  X, 
  Image,
  FileText,
  Code,
  Archive,
  Loader2,
  Mic,
  Square,
  Command
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useFileUpload } from '@/hooks/useFileUpload';
import { FileAttachment } from '@/types';
import toast from 'react-hot-toast';

interface MessageInputProps {
  onSendMessage: (content: string, attachments?: FileAttachment[]) => void;
  onCancelMessage?: () => void;
  isLoading?: boolean;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
}

export function MessageInput({
  onSendMessage,
  onCancelMessage,
  isLoading,
  disabled,
  placeholder = "Type your message... (Shift+Enter for new line)",
  className,
}: MessageInputProps) {
  const [message, setMessage] = useState('');
  const [attachedFiles, setAttachedFiles] = useState<FileAttachment[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  const { getRootProps, getInputProps, isDragActive, uploadFile } = useFileUpload({
    onUploadComplete: (file) => {
      setAttachedFiles((prev) => [...prev, file]);
    },
    onUploadError: (error) => {
      toast.error(`Upload failed: ${error.message}`);
    },
  });
  
  const handleSend = () => {
    if (!message.trim() && attachedFiles.length === 0) return;
    
    onSendMessage(message, attachedFiles);
    setMessage('');
    setAttachedFiles([]);
    textareaRef.current?.focus();
  };
  
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
    
    if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
    }
  };
  
  const removeAttachment = (id: string) => {
    setAttachedFiles((prev) => prev.filter((f) => f.id !== id));
  };
  
  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    for (const file of files) {
      await uploadFile(file);
    }
  };
  
  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return <Image className="h-4 w-4" />;
    if (type.startsWith('text/') || type.includes('document')) return <FileText className="h-4 w-4" />;
    if (type.includes('code') || type.includes('javascript') || type.includes('json')) return <Code className="h-4 w-4" />;
    if (type.includes('zip') || type.includes('archive')) return <Archive className="h-4 w-4" />;
    return <FileText className="h-4 w-4" />;
  };
  
  return (
    <div className={cn('border-t bg-background/95 backdrop-blur', className)}>
      <AnimatePresence>
        {attachedFiles.length > 0 && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-b p-3"
          >
            <div className="flex flex-wrap gap-2">
              {attachedFiles.map((file) => (
                <Card key={file.id} className="flex items-center gap-2 p-2">
                  {getFileIcon(file.type)}
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium truncate">{file.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-6 w-6 p-0"
                    onClick={() => removeAttachment(file.id)}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </Card>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      <div className="p-4">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <div
              {...getRootProps()}
              className={cn(
                'relative',
                isDragActive && 'ring-2 ring-primary ring-offset-2 rounded-lg'
              )}
            >
              <input {...getInputProps()} className="hidden" />
              
              <Textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                disabled={disabled || isLoading}
                className="min-h-[60px] max-h-[200px] pr-12 resize-none"
                rows={1}
              />
              
              {isDragActive && (
                <div className="absolute inset-0 bg-primary/10 rounded-lg flex items-center justify-center">
                  <p className="text-sm font-medium">Drop files here...</p>
                </div>
              )}
            </div>
            
            <div className="absolute bottom-2 right-2 flex gap-1">
              <label htmlFor="file-upload">
                <Button
                  size="sm"
                  variant="ghost"
                  className="h-8 w-8 p-0"
                  disabled={disabled || isLoading}
                  asChild
                >
                  <span>
                    <Paperclip className="h-4 w-4" />
                  </span>
                </Button>
                <input
                  id="file-upload"
                  type="file"
                  multiple
                  className="hidden"
                  onChange={handleFileSelect}
                  disabled={disabled || isLoading}
                />
              </label>
              
              <Button
                size="sm"
                variant="ghost"
                className="h-8 w-8 p-0"
                disabled={disabled || isLoading}
                onClick={() => {
                  setIsRecording(!isRecording);
                  toast(isRecording ? 'Recording stopped' : 'Recording started');
                }}
              >
                {isRecording ? (
                  <Square className="h-4 w-4 text-red-500" />
                ) : (
                  <Mic className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>
          
          <div className="flex flex-col gap-2">
            {isLoading ? (
              <Button
                size="sm"
                variant="destructive"
                onClick={onCancelMessage}
                className="h-[60px]"
              >
                <Square className="h-4 w-4 mr-2" />
                Stop
              </Button>
            ) : (
              <Button
                size="sm"
                onClick={handleSend}
                disabled={disabled || (!message.trim() && attachedFiles.length === 0)}
                className="h-[60px]"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            )}
          </div>
        </div>
        
        <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <kbd className="px-1.5 py-0.5 border rounded text-xs">⌘K</kbd>
            <span>Command palette</span>
          </div>
          <div className="flex items-center gap-2">
            <kbd className="px-1.5 py-0.5 border rounded text-xs">Shift</kbd>
            <span>+</span>
            <kbd className="px-1.5 py-0.5 border rounded text-xs">Enter</kbd>
            <span>New line</span>
          </div>
        </div>
      </div>
    </div>
  );
}