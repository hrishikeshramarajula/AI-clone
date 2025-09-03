import React from 'react';
import { useSettingsStore } from '@/store/settingsStore';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuCheckboxItem,
} from '@/components/ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import {
  Settings,
  User,
  LogOut,
  HelpCircle,
  Keyboard,
  Download,
  Upload,
  RotateCcw,
  Gauge,
  Type,
  Palette,
} from 'lucide-react';
import toast from 'react-hot-toast';

export function SettingsMenu() {
  const settings = useSettingsStore();
  const [dialogOpen, setDialogOpen] = React.useState(false);
  
  const handleExportSettings = () => {
    const data = JSON.stringify(settings, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'scout-settings.json';
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Settings exported');
  };
  
  const handleImportSettings = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) return;
      
      try {
        const text = await file.text();
        const imported = JSON.parse(text);
        settings.updateSettings(imported);
        toast.success('Settings imported');
      } catch (error) {
        toast.error('Failed to import settings');
      }
    };
    input.click();
  };
  
  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button size="sm" variant="ghost" className="h-8 w-8 p-0">
            <Settings className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-56">
          <DropdownMenuLabel>Settings</DropdownMenuLabel>
          <DropdownMenuSeparator />
          
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <User className="mr-2 h-4 w-4" />
              <span>Profile</span>
            </DropdownMenuItem>
            
            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
              <DialogTrigger asChild>
                <DropdownMenuItem onSelect={(e) => e.preventDefault()}>
                  <Gauge className="mr-2 h-4 w-4" />
                  <span>Preferences</span>
                </DropdownMenuItem>
              </DialogTrigger>
            </Dialog>
            
            <DropdownMenuItem>
              <Keyboard className="mr-2 h-4 w-4" />
              <span>Keyboard Shortcuts</span>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          
          <DropdownMenuSeparator />
          
          <DropdownMenuGroup>
            <DropdownMenuCheckboxItem
              checked={settings.streamResponse}
              onCheckedChange={(checked) => settings.updateSettings({ streamResponse: checked })}
            >
              Stream responses
            </DropdownMenuCheckboxItem>
            
            <DropdownMenuCheckboxItem
              checked={settings.showTokenUsage}
              onCheckedChange={(checked) => settings.updateSettings({ showTokenUsage: checked })}
            >
              Show token usage
            </DropdownMenuCheckboxItem>
            
            <DropdownMenuCheckboxItem
              checked={settings.autoSave}
              onCheckedChange={(checked) => settings.updateSettings({ autoSave: checked })}
            >
              Auto-save conversations
            </DropdownMenuCheckboxItem>
            
            <DropdownMenuCheckboxItem
              checked={settings.keyboardShortcuts}
              onCheckedChange={(checked) => settings.updateSettings({ keyboardShortcuts: checked })}
            >
              Enable shortcuts
            </DropdownMenuCheckboxItem>
          </DropdownMenuGroup>
          
          <DropdownMenuSeparator />
          
          <DropdownMenuGroup>
            <DropdownMenuItem onClick={handleExportSettings}>
              <Download className="mr-2 h-4 w-4" />
              <span>Export Settings</span>
            </DropdownMenuItem>
            
            <DropdownMenuItem onClick={handleImportSettings}>
              <Upload className="mr-2 h-4 w-4" />
              <span>Import Settings</span>
            </DropdownMenuItem>
            
            <DropdownMenuItem
              onClick={() => {
                settings.resetSettings();
                toast.success('Settings reset to defaults');
              }}
            >
              <RotateCcw className="mr-2 h-4 w-4" />
              <span>Reset to Defaults</span>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          
          <DropdownMenuSeparator />
          
          <DropdownMenuItem>
            <HelpCircle className="mr-2 h-4 w-4" />
            <span>Help & Support</span>
          </DropdownMenuItem>
          
          <DropdownMenuItem className="text-destructive">
            <LogOut className="mr-2 h-4 w-4" />
            <span>Sign Out</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Preferences</DialogTitle>
            <DialogDescription>
              Customize your Scout AI experience
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6 py-4">
            <div className="space-y-2">
              <Label htmlFor="temperature">
                Temperature: {settings.temperature?.toFixed(1) || '0.7'}
              </Label>
              <Slider
                id="temperature"
                min={0}
                max={2}
                step={0.1}
                value={[settings.temperature || 0.7]}
                onValueChange={([value]) => settings.updateSettings({ temperature: value })}
              />
              <p className="text-xs text-muted-foreground">
                Controls randomness in responses. Lower is more focused, higher is more creative.
              </p>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="maxTokens">
                Max Tokens: {settings.maxTokens || 4000}
              </Label>
              <Slider
                id="maxTokens"
                min={100}
                max={8000}
                step={100}
                value={[settings.maxTokens || 4000]}
                onValueChange={([value]) => settings.updateSettings({ maxTokens: value })}
              />
              <p className="text-xs text-muted-foreground">
                Maximum length of generated responses.
              </p>
            </div>
            
            <div className="space-y-2">
              <Label>Font Size</Label>
              <div className="flex gap-2">
                {(['small', 'medium', 'large'] as const).map((size) => (
                  <Button
                    key={size}
                    variant={settings.fontSize === size ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => settings.updateSettings({ fontSize: size })}
                    className="flex-1"
                  >
                    <Type className={`h-4 w-4 ${
                      size === 'small' ? 'scale-75' : 
                      size === 'large' ? 'scale-125' : ''
                    }`} />
                  </Button>
                ))}
              </div>
            </div>
            
            <div className="space-y-2">
              <Label>Code Theme</Label>
              <div className="flex gap-2">
                {['oneDark', 'github', 'dracula'].map((theme) => (
                  <Button
                    key={theme}
                    variant={settings.codeTheme === theme ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => settings.updateSettings({ codeTheme: theme })}
                    className="flex-1 text-xs"
                  >
                    {theme}
                  </Button>
                ))}
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="stream">Stream Responses</Label>
                <p className="text-xs text-muted-foreground">
                  Show responses as they're generated
                </p>
              </div>
              <Switch
                id="stream"
                checked={settings.streamResponse}
                onCheckedChange={(checked) => settings.updateSettings({ streamResponse: checked })}
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="tokens">Show Token Usage</Label>
                <p className="text-xs text-muted-foreground">
                  Display token count for messages
                </p>
              </div>
              <Switch
                id="tokens"
                checked={settings.showTokenUsage}
                onCheckedChange={(checked) => settings.updateSettings({ showTokenUsage: checked })}
              />
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}