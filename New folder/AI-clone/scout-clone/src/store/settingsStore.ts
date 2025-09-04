import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Settings } from '@/types';

interface SettingsState extends Settings {
  updateSettings: (updates: Partial<Settings>) => void;
  resetSettings: () => void;
}

const defaultSettings: Settings = {
  theme: 'system',
  model: 'claude-3-opus',
  temperature: 0.7,
  maxTokens: 4000,
  streamResponse: true,
  showTokenUsage: true,
  autoSave: true,
  keyboardShortcuts: true,
  fontSize: 'medium',
  codeTheme: 'oneDark',
};

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      ...defaultSettings,
      
      updateSettings: (updates) => {
        set((state) => ({ ...state, ...updates }));
      },
      
      resetSettings: () => {
        set(defaultSettings);
      },
    }),
    {
      name: 'scout-settings-storage',
    }
  )
);