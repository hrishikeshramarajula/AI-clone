class StorageService {
  private prefix = 'scout_';
  
  setItem(key: string, value: any): void {
    try {
      const serialized = JSON.stringify(value);
      localStorage.setItem(this.prefix + key, serialized);
    } catch (error) {
      console.error('Failed to save to localStorage:', error);
    }
  }
  
  getItem<T>(key: string, defaultValue?: T): T | null {
    try {
      const item = localStorage.getItem(this.prefix + key);
      if (item === null) return defaultValue ?? null;
      return JSON.parse(item);
    } catch (error) {
      console.error('Failed to load from localStorage:', error);
      return defaultValue ?? null;
    }
  }
  
  removeItem(key: string): void {
    localStorage.removeItem(this.prefix + key);
  }
  
  clear(): void {
    Object.keys(localStorage)
      .filter((key) => key.startsWith(this.prefix))
      .forEach((key) => localStorage.removeItem(key));
  }
  
  saveConversation(id: string, data: any): void {
    this.setItem(`conversation_${id}`, data);
  }
  
  loadConversation(id: string): any {
    return this.getItem(`conversation_${id}`);
  }
  
  saveSettings(settings: any): void {
    this.setItem('settings', settings);
  }
  
  loadSettings(): any {
    return this.getItem('settings', {
      theme: 'system',
      model: 'claude-3-opus',
      streamResponse: true,
      showTokenUsage: true,
      autoSave: true,
      keyboardShortcuts: true,
      fontSize: 'medium',
      codeTheme: 'oneDark',
    });
  }
  
  saveRecentFiles(files: any[]): void {
    this.setItem('recent_files', files);
  }
  
  loadRecentFiles(): any[] {
    return this.getItem('recent_files', []) || [];
  }
  
  saveCommandHistory(commands: string[]): void {
    this.setItem('command_history', commands.slice(-100));
  }
  
  loadCommandHistory(): string[] {
    return this.getItem('command_history', []) || [];
  }
}

export const storageService = new StorageService();