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
} from 'lucide-react';

interface Task {
  id: string;
  status: 'needs-review' | 'completed';
  timestamp: string;
  content: string;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'active' | 'archived'>('active');
  const [searchQuery, setSearchQuery] = useState('');
  const [showTasks, setShowTasks] = useState(false);
  const [section, setSection] = useState<'triage' | 'task'>('triage');
  const [inputValue, setInputValue] = useState('');
  const [model, setModel] = useState('Qwen 3 Coder');
  const [isModelOpen, setIsModelOpen] = useState(false);
  const [isInputFocused, setIsInputFocused] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const tasks: Task[] = [
    { id: 'SCO-010', status: 'needs-review', timestamp: '7 minutes ago', content: 'addr' },
    { id: 'SCO-009', status: 'needs-review', timestamp: 'Sep 2, 9:26 AM', content: 'hi' },
    { id: 'SCO-008', status: 'needs-review', timestamp: 'Sep 1, 12:26 PM', content: 'Enhance Trading Bot…' },
  ];
  const models = ['Qwen 3 Coder', 'GPT-5', 'Claude 3', 'Gemini Ultra'];
  const activeCount = tasks.filter(t => t.status === 'needs-review').length;

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
          <div className="flex items-center gap-2 mb-4">
            <div className="w-2 h-2 rounded-full bg-[#059669]" />
            <span className="font-medium text-[#0f172a]">Needs review</span>
            <span className="bg-[#e2e8f0] px-2 py-1 rounded-full text-xs text-[#1e293b]">
              {activeCount}
            </span>
          </div>

          {tasks.map(t => (
            <div key={t.id} className="bg-white border-2 border-[#cbd5e1] rounded-lg mb-3 p-3 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-[#475569]" />
                <span className="font-medium text-[#0f172a]">{t.id}</span>
                <span className="text-sm text-[#475569]">{t.timestamp}</span>
              </div>
              <div className="text-sm text-[#334155] mb-2">{t.content}</div>
              <div className="flex justify-between items-center">
                <span className="text-[#059669] font-medium">✓ Completed</span>
                <button className="bg-[#2563eb] text-white px-3 py-1.5 rounded-md hover:bg-[#1d4ed8]">
                  Archive
                </button>
              </div>
            </div>
          ))}
        </section>

        <footer className="p-2 border border-gray-400 border-opacity-60 shadow-lg fixed bottom-5 left-[200px] right-[95px] bg-white z-10 rounded-lg">
          <div className="flex justify-between mb-1">
            <div className="flex gap-2">
              <button
                className={`px-2 py-1 rounded-full text-xs font-medium ${section === 'triage' ? 'bg-[#1e293b] text-white' : 'bg-[#e2e8f0] text-[#1e293b]'}`}
                onClick={() => setSection('triage')}
              >
                ◯ Triage
              </button>
              <button
                className={`px-2 py-1 rounded-full text-xs font-medium ${section === 'task' ? 'bg-[#1e293b] text-white' : 'bg-[#e2e8f0] text-[#1e293b]'}`}
                onClick={() => setSection('task')}
              >
                + Task
              </button>
            </div>
          </div>

          <div className="relative">
            <textarea
              ref={inputRef}
              placeholder="Start creating with the AI"
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onFocus={() => setIsInputFocused(true)}
              onBlur={() => setIsInputFocused(false)}
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
                  <div className="absolute bottom-full left-0 right-0 bg-white border border-[#e2e8f0] rounded-md mb-2">
                    {models.map(m => (
                      <button
                        key={m}
                        className={`w-full px-2 py-1.5 text-left ${m === model ? 'bg-[#ebf8ff]' : ''}`}
                        onClick={() => { setModel(m); setIsModelOpen(false); }}
                      >
                        {m}
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <Send className="w-6 h-6 text-[#1e40af] cursor-pointer" />
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
