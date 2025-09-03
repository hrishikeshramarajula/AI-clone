import React, { useState, useEffect, Suspense } from 'react';
import { Toaster } from 'react-hot-toast';
import { ChatInterface } from '@/components/Chat/ChatInterface';
import { ConversationList } from '@/components/Sidebar/ConversationList';
import { FileExplorer } from '@/components/Sidebar/FileExplorer';
import { TaskManager } from '@/components/Sidebar/TaskManager';
import { Header } from '@/components/Header/Header';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable';
import { Sheet, SheetContent } from '@/components/ui/sheet';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { LoadingScreen } from '@/components/LoadingScreen';
import { cn } from '@/lib/utils';
import { useTheme } from '@/hooks/useTheme';
import { useWebSocket } from '@/hooks/useWebSocket';
import { MessageSquare, FileText, CheckSquare, X } from 'lucide-react';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const { theme } = useTheme();
  const { isConnected } = useWebSocket();
  
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  useEffect(() => {
    if (!isMobile) {
      setSidebarOpen(false);
    }
  }, [isMobile]);
  
  const SidebarContent = () => (
    <Tabs defaultValue="conversations" className="h-full flex flex-col">
      <TabsList className="w-full justify-start rounded-none border-b bg-transparent p-0">
        <TabsTrigger
          value="conversations"
          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent"
        >
          <MessageSquare className="h-4 w-4 mr-2" />
          Chats
        </TabsTrigger>
        <TabsTrigger
          value="files"
          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent"
        >
          <FileText className="h-4 w-4 mr-2" />
          Files
        </TabsTrigger>
        <TabsTrigger
          value="tasks"
          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent"
        >
          <CheckSquare className="h-4 w-4 mr-2" />
          Tasks
        </TabsTrigger>
      </TabsList>
      
      <TabsContent value="conversations" className="flex-1 mt-0">
        <ConversationList />
      </TabsContent>
      
      <TabsContent value="files" className="flex-1 mt-0">
        <FileExplorer />
      </TabsContent>
      
      <TabsContent value="tasks" className="flex-1 mt-0">
        <TaskManager />
      </TabsContent>
    </Tabs>
  );
  
  return (
    <div className="flex h-screen flex-col overflow-hidden bg-background">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="flex-1 overflow-hidden">
        {isMobile ? (
          <>
            <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
              <SheetContent side="left" className="w-80 p-0">
                <div className="flex items-center justify-between p-4 border-b">
                  <h2 className="font-semibold">Navigation</h2>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-8 w-8 p-0"
                    onClick={() => setSidebarOpen(false)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex-1 overflow-hidden">
                  <SidebarContent />
                </div>
              </SheetContent>
            </Sheet>
            
            <ChatInterface className="h-full" />
          </>
        ) : (
          <ResizablePanelGroup direction="horizontal" className="h-full">
            <ResizablePanel
              defaultSize={20}
              minSize={15}
              maxSize={30}
              className="border-r"
            >
              <SidebarContent />
            </ResizablePanel>
            
            <ResizableHandle withHandle />
            
            <ResizablePanel defaultSize={80}>
              <ChatInterface className="h-full" />
            </ResizablePanel>
          </ResizablePanelGroup>
        )}
      </div>
      
      <Toaster
        position="bottom-right"
        toastOptions={{
          className: cn(
            'border',
            theme === 'dark' ? 'bg-background text-foreground' : ''
          ),
          duration: 4000,
        }}
      />
    </div>
  );
}
