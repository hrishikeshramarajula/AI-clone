import React, { useState, useEffect } from 'react';
import { useSettingsStore } from '@/store/settingsStore';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Sparkles, Zap, Brain, Rocket } from 'lucide-react';

interface Model {
  id: string;
  name: string;
  provider: string;
  description: string;
  capabilities: string[];
  icon: React.ReactNode;
  tier: 'free' | 'pro' | 'enterprise';
}

const models: Model[] = [
  {
    id: 'claude-3-opus',
    name: 'Claude 3 Opus',
    provider: 'Anthropic',
    description: 'Most capable model for complex tasks',
    capabilities: ['200K context', 'Advanced reasoning', 'Code generation'],
    icon: <Brain className="h-4 w-4" />,
    tier: 'enterprise',
  },
  {
    id: 'claude-3-sonnet',
    name: 'Claude 3 Sonnet',
    provider: 'Anthropic',
    description: 'Balanced performance and speed',
    capabilities: ['200K context', 'Fast responses', 'Cost-effective'],
    icon: <Zap className="h-4 w-4" />,
    tier: 'pro',
  },
  {
    id: 'claude-3-haiku',
    name: 'Claude 3 Haiku',
    provider: 'Anthropic',
    description: 'Fastest model for simple tasks',
    capabilities: ['200K context', 'Instant responses', 'High volume'],
    icon: <Rocket className="h-4 w-4" />,
    tier: 'free',
  },
  {
    id: 'gpt-4-turbo',
    name: 'GPT-4 Turbo',
    provider: 'OpenAI',
    description: 'Latest GPT-4 with vision',
    capabilities: ['128K context', 'Vision', 'Function calling'],
    icon: <Sparkles className="h-4 w-4" />,
    tier: 'pro',
  },
  {
    id: 'gpt-4',
    name: 'GPT-4',
    provider: 'OpenAI',
    description: 'Advanced reasoning and creativity',
    capabilities: ['32K context', 'Reliable', 'Well-tested'],
    icon: <Brain className="h-4 w-4" />,
    tier: 'pro',
  },
  {
    id: 'gpt-3.5-turbo',
    name: 'GPT-3.5 Turbo',
    provider: 'OpenAI',
    description: 'Fast and cost-effective',
    capabilities: ['16K context', 'Fast', 'Affordable'],
    icon: <Zap className="h-4 w-4" />,
    tier: 'free',
  },
];

export function ModelSelector() {
  const { model, updateSettings } = useSettingsStore();
  const [selectedModel, setSelectedModel] = useState(model);
  
  useEffect(() => {
    setSelectedModel(model);
  }, [model]);
  
  const handleModelChange = (modelId: string) => {
    setSelectedModel(modelId);
    updateSettings({ model: modelId });
  };
  
  const getTierBadge = (tier: Model['tier']) => {
    switch (tier) {
      case 'free':
        return <Badge variant="secondary" className="text-xs">Free</Badge>;
      case 'pro':
        return <Badge variant="default" className="text-xs">Pro</Badge>;
      case 'enterprise':
        return <Badge className="text-xs bg-gradient-to-r from-purple-500 to-pink-500">Enterprise</Badge>;
    }
  };
  
  const currentModel = models.find((m) => m.id === selectedModel);
  
  return (
    <Select value={selectedModel} onValueChange={handleModelChange}>
      <SelectTrigger className="w-[200px]">
        <SelectValue>
          {currentModel && (
            <div className="flex items-center gap-2">
              {currentModel.icon}
              <span className="truncate">{currentModel.name}</span>
            </div>
          )}
        </SelectValue>
      </SelectTrigger>
      <SelectContent className="w-[320px]">
        <SelectGroup>
          <SelectLabel>Available Models</SelectLabel>
          {models.map((model) => (
            <SelectItem key={model.id} value={model.id} className="py-3">
              <div className="flex items-start gap-3 w-full">
                <div className="mt-0.5">{model.icon}</div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{model.name}</span>
                    {getTierBadge(model.tier)}
                  </div>
                  <p className="text-xs text-muted-foreground">{model.description}</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {model.capabilities.map((cap) => (
                      <Badge key={cap} variant="outline" className="text-xs py-0">
                        {cap}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}