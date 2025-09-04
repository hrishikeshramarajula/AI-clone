'use client';
import React, { useState, useRef } from 'react';
import {
  Search,
  ChevronDown,
  Calendar,
  FileText,
  Globe,
  Settings,
  Archive,
  Send,
  ChevronUp,
  Sparkles,
  Loader2,
  Brain,
  Code,
  BarChart3,
  MessageSquare,
} from 'lucide-react';

interface Task {
  id: string;
  status: 'needs-review' | 'completed';
  timestamp: string;
  content: string;
}

interface AIModel {
  id: string;
  name: string;
  provider: string;
  description: string;
  apiModel?: string;
  intelligence?: string;
  contextLength?: string;
  inputCredits?: string;
  outputCredits?: string;
}

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
  model?: string;
  searchResults?: any[];
}

interface SearchResult {
  url: string;
  name: string;
  snippet: string;
  host_name: string;
  rank: number;
  date: string;
  favicon: string;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<'active' | 'archived'>('active');
  const [searchQuery, setSearchQuery] = useState('');
  const [showTasks, setShowTasks] = useState(false);
  const [section, setSection] = useState<'triage' | 'task'>('triage');
  const [inputValue, setInputValue] = useState('');
  const [model, setModel] = useState('GPT-4');
  const [isModelOpen, setIsModelOpen] = useState(false);
  const [isInputFocused, setIsInputFocused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [chatMode, setChatMode] = useState<'chat' | 'search' | 'code' | 'analysis'>('chat');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const models: AIModel[] = [
    { 
      id: 'gpt-4', 
      name: 'GPT-4', 
      provider: 'OpenAI', 
      description: 'Most capable model', 
      apiModel: 'gpt-4',
      intelligence: 'High',
      contextLength: '128K',
      inputCredits: '10K',
      outputCredits: '30K'
    },
    { 
      id: 'glm-4.5', 
      name: 'GLM-4.5', 
      provider: 'Zhipu AI', 
      description: 'Latest Chinese AI model', 
      apiModel: 'glm-4.5',
      intelligence: 'Very High',
      contextLength: '200K',
      inputCredits: '8K',
      outputCredits: '25K'
    },
    { 
      id: 'gpt-3.5-turbo', 
      name: 'GPT-3.5 Turbo', 
      provider: 'OpenAI', 
      description: 'Fast and efficient', 
      apiModel: 'gpt-3.5-turbo',
      intelligence: 'Medium',
      contextLength: '16K',
      inputCredits: '5K',
      outputCredits: '15K'
    },
    { 
      id: 'claude-3-opus', 
      name: 'Claude 3 Opus', 
      provider: 'Anthropic', 
      description: 'Advanced reasoning', 
      apiModel: 'claude-3-opus',
      intelligence: 'Very High',
      contextLength: '200K',
      inputCredits: '15K',
      outputCredits: '75K'
    },
    { 
      id: 'claude-3-sonnet', 
      name: 'Claude 3 Sonnet', 
      provider: 'Anthropic', 
      description: 'Balanced performance', 
      apiModel: 'claude-3-sonnet',
      intelligence: 'High',
      contextLength: '200K',
      inputCredits: '3K',
      outputCredits: '15K'
    },
    { 
      id: 'gemini-pro', 
      name: 'Gemini Pro', 
      provider: 'Google', 
      description: 'Multimodal capabilities', 
      apiModel: 'gemini-pro',
      intelligence: 'High',
      contextLength: '32K',
      inputCredits: 'Free',
      outputCredits: 'Free'
    },
    { 
      id: 'llama-3-70b', 
      name: 'Llama 3 70B', 
      provider: 'Meta', 
      description: 'Open source powerhouse', 
      apiModel: 'llama-3-70b',
      intelligence: 'High',
      contextLength: '8K',
      inputCredits: 'Free',
      outputCredits: 'Free'
    },
    { 
      id: 'mixtral-8x7b', 
      name: 'Mixtral 8x7B', 
      provider: 'Mistral', 
      description: 'Mixture of experts', 
      apiModel: 'mixtral-8x7b',
      intelligence: 'High',
      contextLength: '32K',
      inputCredits: 'Free',
      outputCredits: 'Free'
    },
    { 
      id: 'command-r-plus', 
      name: 'Command R+', 
      provider: 'Cohere', 
      description: 'Enterprise grade', 
      apiModel: 'command-r-plus',
      intelligence: 'High',
      contextLength: '128K',
      inputCredits: '5K',
      outputCredits: '15K'
    }
  ];

  const tasks: Task[] = [
    { id: 'SCO-010', status: 'needs-review', timestamp: '7 minutes ago', content: 'addr' },
    { id: 'SCO-009', status: 'needs-review', timestamp: 'Sep 2, 9:26 AM', content: 'hi' },
    { id: 'SCO-008', status: 'needs-review', timestamp: 'Sep 1, 12:26 PM', content: 'Enhance Trading Bot…' },
  ];
  const activeCount = tasks.filter(t => t.status === 'needs-review').length;

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    console.log('Sending message:', { message: inputValue, model, chatMode });

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
          model,
          searchType: chatMode,
        }),
      });

      console.log('API response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('API error response:', errorData);
        throw new Error(errorData.error || 'Failed to get AI response');
      }

      const data = await response.json();
      console.log('API response data:', data);
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        model: data.model,
        searchResults: data.searchResults,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const getModeIcon = (mode: string) => {
    switch (mode) {
      case 'search': return <Search className="w-4 h-4" />;
      case 'code': return <Code className="w-4 h-4" />;
      case 'analysis': return <BarChart3 className="w-4 h-4" />;
      default: return <MessageSquare className="w-4 h-4" />;
    }
  };

  const getModeLabel = (mode: string) => {
    switch (mode) {
      case 'search': return 'Web Search';
      case 'code': return 'Code Generation';
      case 'analysis': return 'Analysis';
      default: return 'Chat';
    }
  };

  return (
    <div className={`flex h-[75vh] ${isInputFocused ? 'blur-bg' : ''}`}>
      {/* Sidebar */}
      <aside className="w-[195px] bg-white border-r border-[#e2e8f0] flex flex-col">
        <div className="flex items-center p-3 gap-2">
          <div className="bg-[#3b82f6] text-white w-8 h-8 rounded-md flex items-center justify-center font-semibold">
            B
          </div>
          <span className="font-medium text-[#1e293b]">BOT</span>
          <ChevronDown className="text-[#64748b]" />
        </div>

        <div className="relative px-3 mb-3">
          <Search className="absolute top-1/2 left-6 transform -translate-y-1/2 text-[#64748b]" />
          <input
            type="text"
            placeholder="Search"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="w-full px-8 py-2 border border-[#e2e8f0] rounded-md"
          />
          <span className="absolute top-1/2 right-6 transform -translate-y-1/2 bg-[#f1f5f9] px-2 py-1 rounded text-xs text-[#64748b]">
            ⌘K
          </span>
        </div>

        <nav className="flex flex-col gap-1 px-3">
          <button className="flex items-center gap-2 p-2 text-[#475569] hover:bg-[#f1f5f9] hover:text-[#1e293b]">
            <Calendar className="w-4 h-4" />
            <span>Tasks</span>
          </button>
          <button className="flex items-center gap-2 p-2 text-[#475569] hover:bg-[#f1f5f9] hover:text-[#1e293b]">
            <FileText className="w-4 h-4" />
            <span>Files</span>
          </button>
          <button className="flex items-center gap-2 p-2 text-[#475569] hover:bg-[#f1f5f9] hover:text-[#1e293b]">
            <Globe className="w-4 h-4" />
            <span>Apps</span>
          </button>
          <button className="flex items-center gap-2 p-2 text-[#475569] hover:bg-[#f1f5f9] hover:text-[#1e293b]">
            <Settings className="w-4 h-4" />
            <span>Configuration</span>
          </button>
        </nav>

        <div className="px-3 mt-auto">
          <button
            className="flex items-center gap-1.5 text-[#475569] font-medium"
            onClick={() => setShowTasks(!showTasks)}
          >
            <ChevronDown className="text-[#64748b]" />
            Active tasks ({activeCount})
          </button>
          {showTasks && (
            <div className="mt-2 flex flex-col gap-2">
              {tasks.map(t => (
                <div key={t.id} className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-[#10b981]" />
                  <div className="text-xs text-[#475569]">
                    <div className="font-medium">Needs review</div>
                    <div className="text-[#64748b]">{t.timestamp}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col bg-white">
        <header className={`flex items-center p-3 border-b border-[#e2e8f0] gap-4 ${isInputFocused ? 'invisible' : ''}`}>
          <button
            className={`pb-1 cursor-pointer ${activeTab === 'active' ? 'text-[#1e293b] border-b-2 border-[#1e293b]' : 'text-[#94a3b8]'}`}
            onClick={() => setActiveTab('active')}
          >
            Active
          </button>
          <button
            className={`pb-1 cursor-pointer ${activeTab === 'archived' ? 'text-[#1e293b] border-b-2 border-[#1e293b]' : 'text-[#94a3b8]'}`}
            onClick={() => setActiveTab('archived')}
          >
            Archived
          </button>
          <div className="ml-auto text-[#64748b]">Display</div>
        </header>

        <section className={`flex-1 overflow-y-auto p-3 bg-[#f8fafc] ${isInputFocused ? 'invisible' : ''} pb-24`}>
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <Brain className="w-16 h-16 text-[#3b82f6] mb-4" />
              <h2 className="text-2xl font-bold text-[#1e293b] mb-2">AI Search Engine</h2>
              <p className="text-[#64748b] mb-6">Ask anything and get intelligent responses with web search capabilities</p>
              <div className="grid grid-cols-2 gap-4 max-w-md">
                <button
                  onClick={() => setChatMode('chat')}
                  className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 ${
                    chatMode === 'chat' 
                      ? 'border-[#3b82f6] bg-[#eff6ff]' 
                      : 'border-[#e2e8f0] hover:border-[#cbd5e1]'
                  }`}
                >
                  <MessageSquare className="w-6 h-6 text-[#3b82f6]" />
                  <span className="text-sm font-medium">Chat</span>
                </button>
                <button
                  onClick={() => setChatMode('search')}
                  className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 ${
                    chatMode === 'search' 
                      ? 'border-[#3b82f6] bg-[#eff6ff]' 
                      : 'border-[#e2e8f0] hover:border-[#cbd5e1]'
                  }`}
                >
                  <Search className="w-6 h-6 text-[#3b82f6]" />
                  <span className="text-sm font-medium">Web Search</span>
                </button>
                <button
                  onClick={() => setChatMode('code')}
                  className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 ${
                    chatMode === 'code' 
                      ? 'border-[#3b82f6] bg-[#eff6ff]' 
                      : 'border-[#e2e8f0] hover:border-[#cbd5e1]'
                  }`}
                >
                  <Code className="w-6 h-6 text-[#3b82f6]" />
                  <span className="text-sm font-medium">Code</span>
                </button>
                <button
                  onClick={() => setChatMode('analysis')}
                  className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 ${
                    chatMode === 'analysis' 
                      ? 'border-[#3b82f6] bg-[#eff6ff]' 
                      : 'border-[#e2e8f0] hover:border-[#cbd5e1]'
                  }`}
                >
                  <BarChart3 className="w-6 h-6 text-[#3b82f6]" />
                  <span className="text-sm font-medium">Analysis</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {message.type === 'assistant' && (
                    <div className="w-8 h-8 bg-[#3b82f6] rounded-full flex items-center justify-center flex-shrink-0">
                      <Brain className="w-4 h-4 text-white" />
                    </div>
                  )}
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.type === 'user'
                        ? 'bg-[#3b82f6] text-white'
                        : 'bg-white border border-[#e2e8f0]'
                    }`}
                  >
                    <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                    {message.model && (
                      <div className="text-xs mt-2 opacity-70">
                        {message.model} • {new Date(message.timestamp).toLocaleTimeString()}
                      </div>
                    )}
                    {message.searchResults && message.searchResults.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-[#e2e8f0]">
                        <div className="text-xs font-medium mb-2 text-[#64748b]">Search Results:</div>
                        {message.searchResults.slice(0, 3).map((result: SearchResult, index: number) => (
                          <div key={index} className="mb-2 p-2 bg-[#f8fafc] rounded text-xs">
                            <div className="font-medium text-[#1e293b]">{result.name}</div>
                            <div className="text-[#64748b] mt-1">{result.snippet}</div>
                            <div className="text-[#94a3b8] mt-1">{result.host_name}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                  {message.type === 'user' && (
                    <div className="w-8 h-8 bg-[#64748b] rounded-full flex items-center justify-center flex-shrink-0">
                      <span className="text-white text-sm font-medium">U</span>
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 bg-[#3b82f6] rounded-full flex items-center justify-center flex-shrink-0">
                    <Brain className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-white border border-[#e2e8f0] rounded-lg p-3">
                    <Loader2 className="w-4 h-4 animate-spin text-[#3b82f6]" />
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        <footer className="p-2 border border-gray-400 border-opacity-60 shadow-lg fixed bottom-5 left-[200px] right-[95px] bg-white z-10 rounded-lg">
          <div className="flex justify-between mb-1">
            <div className="flex gap-2">
              <button
                className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
                  chatMode === 'chat' ? 'bg-[#1e293b] text-white' : 'bg-[#e2e8f0] text-[#1e293b]'
                }`}
                onClick={() => setChatMode('chat')}
              >
                {getModeIcon('chat')}
                Chat
              </button>
              <button
                className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
                  chatMode === 'search' ? 'bg-[#1e293b] text-white' : 'bg-[#e2e8f0] text-[#1e293b]'
                }`}
                onClick={() => setChatMode('search')}
              >
                {getModeIcon('search')}
                Search
              </button>
              <button
                className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
                  chatMode === 'code' ? 'bg-[#1e293b] text-white' : 'bg-[#e2e8f0] text-[#1e293b]'
                }`}
                onClick={() => setChatMode('code')}
              >
                {getModeIcon('code')}
                Code
              </button>
              <button
                className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
                  chatMode === 'analysis' ? 'bg-[#1e293b] text-white' : 'bg-[#e2e8f0] text-[#1e293b]'
                }`}
                onClick={() => setChatMode('analysis')}
              >
                {getModeIcon('analysis')}
                Analysis
              </button>
            </div>
          </div>

          <div className="relative">
            <textarea
              ref={inputRef}
              placeholder={`Start ${getModeLabel(chatMode).toLowerCase()} with the AI...`}
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onFocus={() => setIsInputFocused(true)}
              onBlur={() => setIsInputFocused(false)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              className="w-full border border-[#e2e8f0] rounded-[2.5rem] p-1 pl-2 resize-none outline-none"
              rows={1}
            />
            <div className="flex justify-between items-center mt-1">
              <div className="relative">
                <button
                  onClick={() => setIsModelOpen(!isModelOpen)}
                  className="flex items-center gap-1 bg-[#bfdbfe] border-2 border-[#3b82f6] px-2.5 py-0.5 rounded-md text-xs text-[#1e40af]"
                >
                  <Sparkles className="w-3 h-3" />
                  {model}
                  <ChevronUp className={`w-3 h-3 ${isModelOpen ? 'rotate-180' : ''}`} />
                </button>
                {isModelOpen && (
                  <div className="absolute bottom-full left-0 right-0 bg-white border border-[#e2e8f0] rounded-lg mb-2 max-h-96 overflow-y-auto shadow-xl z-20">
                    <div className="p-3 border-b border-[#e2e8f0] bg-gray-50">
                      <h3 className="font-semibold text-sm text-[#1e293b]">Select AI Model</h3>
                      <p className="text-xs text-[#64748b]">Choose the best model for your task</p>
                    </div>
                    {models.map(m => (
                      <button
                        key={m.id}
                        className={`w-full px-4 py-3 text-left hover:bg-[#f8fafc] border-b border-[#f1f5f9] last:border-b-0 ${
                          model === m.name ? 'bg-[#eff6ff] border-l-4 border-l-[#3b82f6]' : ''
                        }`}
                        onClick={() => { setModel(m.name); setIsModelOpen(false); }}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <div className="font-medium text-sm text-[#1e293b]">{m.name}</div>
                              <div className="px-2 py-0.5 bg-[#dbeafe] text-[#1e40af] text-xs rounded-full">
                                {m.intelligence}
                              </div>
                            </div>
                            <div className="text-xs text-[#64748b] mb-2">{m.provider} • {m.description}</div>
                            <div className="flex items-center gap-4 text-xs text-[#64748b]">
                              <div className="flex items-center gap-1">
                                <span className="font-medium">Context:</span>
                                <span>{m.contextLength}</span>
                              </div>
                              <div className="flex items-center gap-1">
                                <span className="font-medium">Input:</span>
                                <span className={m.inputCredits === 'Free' ? 'text-green-600' : 'text-orange-600'}>
                                  {m.inputCredits}
                                </span>
                              </div>
                              <div className="flex items-center gap-1">
                                <span className="font-medium">Output:</span>
                                <span className={m.outputCredits === 'Free' ? 'text-green-600' : 'text-orange-600'}>
                                  {m.outputCredits}
                                </span>
                              </div>
                            </div>
                          </div>
                          {model === m.name && (
                            <div className="w-5 h-5 bg-[#3b82f6] rounded-full flex items-center justify-center ml-2">
                              <div className="w-2 h-2 bg-white rounded-full"></div>
                            </div>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isLoading}
                className={`w-6 h-6 rounded-full flex items-center justify-center ${
                  inputValue.trim() && !isLoading
                    ? 'text-[#1e40af] cursor-pointer'
                    : 'text-[#94a3b8] cursor-not-allowed'
                }`}
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
