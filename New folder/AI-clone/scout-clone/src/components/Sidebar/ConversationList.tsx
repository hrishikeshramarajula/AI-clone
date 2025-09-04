import React, { useState } from 'react';
import { format } from 'date-fns';
import { motion, AnimatePresence } from 'framer-motion';
import { useChatStore } from '@/store/chatStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Plus, 
  Search, 
  MessageSquare, 
  Pin,
  Archive,
  Trash2,
  MoreHorizontal,
  Edit2,
  Check,
  X
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { Conversation } from '@/types';

export function ConversationList() {
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  
  const {
    conversations,
    currentConversationId,
    setCurrentConversation,
    addConversation,
    deleteConversation,
  } = useChatStore();
  
  const filteredConversations = conversations.filter((conv) =>
    conv.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    conv.messages.some((msg) =>
      msg.content.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );
  
  const handleCreateConversation = () => {
    const newConversation: Conversation = {
      id: `conv_${Date.now()}`,
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    addConversation(newConversation);
  };
  
  const handleEditTitle = (conv: Conversation) => {
    setEditingId(conv.id);
    setEditTitle(conv.title);
  };
  
  const handleSaveTitle = (convId: string) => {
    const conv = conversations.find((c) => c.id === convId);
    if (conv && editTitle.trim()) {
      useChatStore.getState().updateConversationTitle(convId, editTitle.trim());
    }
    setEditingId(null);
    setEditTitle('');
  };
  
  const handlePinConversation = (convId: string) => {
    const conv = conversations.find((c) => c.id === convId);
    if (conv) {
      if (conv.pinned) {
        useChatStore.getState().unpinConversation(convId);
      } else {
        useChatStore.getState().pinConversation(convId);
      }
    }
  };
  
  const handleArchiveConversation = (convId: string) => {
    const conv = conversations.find((c) => c.id === convId);
    if (conv) {
      if (conv.archived) {
        useChatStore.getState().unarchiveConversation(convId);
      } else {
        useChatStore.getState().archiveConversation(convId);
      }
    }
  };
  
  const pinnedConversations = filteredConversations.filter((c) => c.pinned && !c.archived);
  const regularConversations = filteredConversations.filter((c) => !c.pinned && !c.archived);
  const archivedConversations = filteredConversations.filter((c) => c.archived);
  
  const ConversationItem = ({ conversation }: { conversation: Conversation }) => {
    const isActive = currentConversationId === conversation.id;
    const isEditing = editingId === conversation.id;
    
    return (
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        className={cn(
          'group relative flex items-center gap-3 rounded-lg px-3 py-2 hover:bg-muted transition-colors cursor-pointer',
          isActive && 'bg-muted'
        )}
        onClick={() => !isEditing && setCurrentConversation(conversation.id)}
      >
        <MessageSquare className="h-4 w-4 text-muted-foreground shrink-0" />
        
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="flex items-center gap-1">
              <Input
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleSaveTitle(conversation.id);
                  if (e.key === 'Escape') setEditingId(null);
                }}
                className="h-6 text-sm"
                autoFocus
                onClick={(e) => e.stopPropagation()}
              />
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={(e) => {
                  e.stopPropagation();
                  handleSaveTitle(conversation.id);
                }}
              >
                <Check className="h-3 w-3" />
              </Button>
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={(e) => {
                  e.stopPropagation();
                  setEditingId(null);
                }}
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          ) : (
            <>
              <p className="text-sm font-medium truncate">{conversation.title}</p>
              <p className="text-xs text-muted-foreground">
                {format(new Date(conversation.updatedAt), 'MMM d, HH:mm')}
              </p>
            </>
          )}
        </div>
        
        {conversation.pinned && <Pin className="h-3 w-3 text-muted-foreground" />}
        
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              size="sm"
              variant="ghost"
              className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100"
              onClick={(e) => e.stopPropagation()}
            >
              <MoreHorizontal className="h-3 w-3" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => handleEditTitle(conversation)}>
              <Edit2 className="h-3 w-3 mr-2" />
              Rename
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => handlePinConversation(conversation.id)}>
              <Pin className="h-3 w-3 mr-2" />
              {conversation.pinned ? 'Unpin' : 'Pin'}
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => handleArchiveConversation(conversation.id)}>
              <Archive className="h-3 w-3 mr-2" />
              {conversation.archived ? 'Unarchive' : 'Archive'}
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-destructive"
              onClick={() => deleteConversation(conversation.id)}
            >
              <Trash2 className="h-3 w-3 mr-2" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </motion.div>
    );
  };
  
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 space-y-3">
        <Button onClick={handleCreateConversation} className="w-full">
          <Plus className="h-4 w-4 mr-2" />
          New Chat
        </Button>
        
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search conversations..."
            className="pl-9"
          />
        </div>
      </div>
      
      <ScrollArea className="flex-1 px-2">
        <div className="space-y-4 pb-4">
          {pinnedConversations.length > 0 && (
            <div className="space-y-1">
              <p className="text-xs font-medium text-muted-foreground px-3">Pinned</p>
              <AnimatePresence>
                {pinnedConversations.map((conv) => (
                  <ConversationItem key={conv.id} conversation={conv} />
                ))}
              </AnimatePresence>
            </div>
          )}
          
          {regularConversations.length > 0 && (
            <div className="space-y-1">
              {pinnedConversations.length > 0 && (
                <p className="text-xs font-medium text-muted-foreground px-3">Recent</p>
              )}
              <AnimatePresence>
                {regularConversations.map((conv) => (
                  <ConversationItem key={conv.id} conversation={conv} />
                ))}
              </AnimatePresence>
            </div>
          )}
          
          {archivedConversations.length > 0 && (
            <div className="space-y-1">
              <p className="text-xs font-medium text-muted-foreground px-3">Archived</p>
              <AnimatePresence>
                {archivedConversations.map((conv) => (
                  <ConversationItem key={conv.id} conversation={conv} />
                ))}
              </AnimatePresence>
            </div>
          )}
          
          {filteredConversations.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <p className="text-sm">No conversations found</p>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}