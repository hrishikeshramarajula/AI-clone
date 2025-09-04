import React from 'react';
import { ModelSelector } from './ModelSelector';
import { SettingsMenu } from './SettingsMenu';
import { ConnectionStatus } from '@/components/ConnectionStatus';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useTheme } from '@/hooks/useTheme';
import { useChatStore } from '@/store/chatStore';
import { 
  Menu,
  Zap,
  Moon,
  Sun,
  Monitor
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface HeaderProps {
  onMenuClick?: () => void;
  className?: string;
}

export function Header({ onMenuClick, className }: HeaderProps) {
  const { theme, toggleTheme } = useTheme();
  const currentConversation = useChatStore((state) => state.getCurrentConversation());
  
  const getThemeIcon = () => {
    switch (theme) {
      case 'dark':
        return <Moon className="h-4 w-4" />;
      case 'light':
        return <Sun className="h-4 w-4" />;
      default:
        return <Monitor className="h-4 w-4" />;
    }
  };
  
  return (
    <header className={cn(
      'border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60',
      className
    )}>
      <div className="flex items-center justify-between h-14 px-4">
        <div className="flex items-center gap-3">
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0 md:hidden"
            onClick={onMenuClick}
          >
            <Menu className="h-4 w-4" />
          </Button>
          
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-primary" />
            <span className="font-semibold text-lg">Scout AI</span>
            <Badge variant="secondary" className="text-xs">Clone</Badge>
          </div>
          
          {currentConversation && (
            <div className="hidden md:flex items-center gap-2 ml-4 pl-4 border-l">
              <span className="text-sm text-muted-foreground">Current:</span>
              <span className="text-sm font-medium">{currentConversation.title}</span>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-2">
          <ConnectionStatus />
          
          <ModelSelector />
          
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0"
            onClick={toggleTheme}
          >
            {getThemeIcon()}
          </Button>
          
          <SettingsMenu />
        </div>
      </div>
    </header>
  );
}