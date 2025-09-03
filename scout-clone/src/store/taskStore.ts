import { create } from 'zustand';
import { Task } from '@/types';

interface TaskState {
  tasks: Task[];
  activeTaskId: string | null;
  
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  removeTask: (id: string) => void;
  setActiveTask: (id: string | null) => void;
  clearTasks: () => void;
  getActiveTasks: () => Task[];
  getCompletedTasks: () => Task[];
}

export const useTaskStore = create<TaskState>((set, get) => ({
  tasks: [],
  activeTaskId: null,
  
  addTask: (task) => {
    set((state) => ({
      tasks: [...state.tasks, task],
    }));
  },
  
  updateTask: (id, updates) => {
    set((state) => ({
      tasks: state.tasks.map((task) =>
        task.id === id ? { ...task, ...updates } : task
      ),
    }));
  },
  
  removeTask: (id) => {
    set((state) => ({
      tasks: state.tasks.filter((task) => task.id !== id),
      activeTaskId: state.activeTaskId === id ? null : state.activeTaskId,
    }));
  },
  
  setActiveTask: (id) => {
    set({ activeTaskId: id });
  },
  
  clearTasks: () => {
    set({ tasks: [], activeTaskId: null });
  },
  
  getActiveTasks: () => {
    return get().tasks.filter((task) => 
      task.status === 'pending' || task.status === 'in_progress'
    );
  },
  
  getCompletedTasks: () => {
    return get().tasks.filter((task) => 
      task.status === 'completed' || task.status === 'cancelled'
    );
  },
}));