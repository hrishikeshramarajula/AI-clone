import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTaskStore } from '@/store/taskStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  CheckCircle2,
  Circle,
  Clock,
  XCircle,
  Plus,
  Trash2,
  PlayCircle,
  PauseCircle,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  Filter
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';
import { Task } from '@/types';
import { format } from 'date-fns';

export function TaskManager() {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [expandedTasks, setExpandedTasks] = useState<Set<string>>(new Set());
  
  const {
    tasks,
    activeTaskId,
    addTask,
    updateTask,
    removeTask,
    setActiveTask,
    clearTasks,
    getActiveTasks,
    getCompletedTasks,
  } = useTaskStore();
  
  const handleAddTask = () => {
    if (!newTaskTitle.trim()) return;
    
    const newTask: Task = {
      id: `task_${Date.now()}`,
      title: newTaskTitle.trim(),
      status: 'pending',
      createdAt: new Date(),
    };
    
    addTask(newTask);
    setNewTaskTitle('');
  };
  
  const handleToggleTask = (task: Task) => {
    if (task.status === 'completed') {
      updateTask(task.id, { status: 'pending', completedAt: undefined });
    } else {
      updateTask(task.id, { status: 'completed', completedAt: new Date() });
    }
  };
  
  const handleStartTask = (taskId: string) => {
    updateTask(taskId, { status: 'in_progress' });
    setActiveTask(taskId);
  };
  
  const handlePauseTask = (taskId: string) => {
    updateTask(taskId, { status: 'pending' });
    if (activeTaskId === taskId) {
      setActiveTask(null);
    }
  };
  
  const toggleTaskExpanded = (taskId: string) => {
    setExpandedTasks((prev) => {
      const next = new Set(prev);
      if (next.has(taskId)) {
        next.delete(taskId);
      } else {
        next.add(taskId);
      }
      return next;
    });
  };
  
  const getStatusIcon = (status: Task['status']) => {
    switch (status) {
      case 'pending':
        return <Circle className="h-4 w-4 text-muted-foreground" />;
      case 'in_progress':
        return <Clock className="h-4 w-4 text-blue-500 animate-pulse" />;
      case 'completed':
        return <CheckCircle2 className="h-4 w-4 text-green-500" />;
      case 'cancelled':
        return <XCircle className="h-4 w-4 text-red-500" />;
    }
  };
  
  const getStatusBadge = (status: Task['status']) => {
    const variants: Record<Task['status'], 'default' | 'secondary' | 'destructive' | 'outline'> = {
      pending: 'outline',
      in_progress: 'default',
      completed: 'secondary',
      cancelled: 'destructive',
    };
    
    return (
      <Badge variant={variants[status]} className="text-xs">
        {status.replace('_', ' ')}
      </Badge>
    );
  };
  
  const filteredTasks = (() => {
    switch (filter) {
      case 'active':
        return getActiveTasks();
      case 'completed':
        return getCompletedTasks();
      default:
        return tasks;
    }
  })();
  
  const TaskItem = ({ task }: { task: Task }) => {
    const isExpanded = expandedTasks.has(task.id);
    const isActive = activeTaskId === task.id;
    
    return (
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        className={cn(
          'border rounded-lg p-3 space-y-2',
          isActive && 'border-primary bg-primary/5'
        )}
      >
        <div className="flex items-start gap-2">
          <button
            className="mt-0.5"
            onClick={() => handleToggleTask(task)}
            disabled={task.status === 'in_progress'}
          >
            {getStatusIcon(task.status)}
          </button>
          
          <div className="flex-1 space-y-1">
            <div className="flex items-center gap-2">
              <p className={cn(
                'text-sm font-medium',
                task.status === 'completed' && 'line-through text-muted-foreground'
              )}>
                {task.title}
              </p>
              {getStatusBadge(task.status)}
            </div>
            
            {task.description && (
              <p className="text-xs text-muted-foreground">{task.description}</p>
            )}
            
            {task.progress !== undefined && (
              <Progress value={task.progress} className="h-2" />
            )}
            
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span>Created: {format(new Date(task.createdAt), 'MMM d, HH:mm')}</span>
              {task.completedAt && (
                <span>Completed: {format(new Date(task.completedAt), 'MMM d, HH:mm')}</span>
              )}
            </div>
          </div>
          
          <div className="flex gap-1">
            {task.status === 'pending' && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={() => handleStartTask(task.id)}
              >
                <PlayCircle className="h-3 w-3" />
              </Button>
            )}
            
            {task.status === 'in_progress' && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={() => handlePauseTask(task.id)}
              >
                <PauseCircle className="h-3 w-3" />
              </Button>
            )}
            
            {task.description && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 w-6 p-0"
                onClick={() => toggleTaskExpanded(task.id)}
              >
                {isExpanded ? (
                  <ChevronUp className="h-3 w-3" />
                ) : (
                  <ChevronDown className="h-3 w-3" />
                )}
              </Button>
            )}
            
            <Button
              size="sm"
              variant="ghost"
              className="h-6 w-6 p-0"
              onClick={() => removeTask(task.id)}
            >
              <Trash2 className="h-3 w-3" />
            </Button>
          </div>
        </div>
        
        {isExpanded && task.description && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="pt-2 border-t"
          >
            <p className="text-sm">{task.description}</p>
          </motion.div>
        )}
      </motion.div>
    );
  };
  
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 space-y-3">
        <div className="flex gap-2">
          <Input
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="New task..."
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleAddTask();
            }}
          />
          <Button size="sm" onClick={handleAddTask}>
            <Plus className="h-4 w-4" />
          </Button>
        </div>
        
        <div className="flex items-center justify-between">
          <Select value={filter} onValueChange={(v) => setFilter(v as typeof filter)}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Tasks</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="completed">Completed</SelectItem>
            </SelectContent>
          </Select>
          
          <div className="flex gap-1">
            <Button
              size="sm"
              variant="ghost"
              className="h-7 px-2"
              onClick={() => window.location.reload()}
            >
              <RefreshCw className="h-3 w-3 mr-1" />
              Refresh
            </Button>
            {tasks.length > 0 && (
              <Button
                size="sm"
                variant="ghost"
                className="h-7 px-2"
                onClick={clearTasks}
              >
                Clear All
              </Button>
            )}
          </div>
        </div>
      </div>
      
      <ScrollArea className="flex-1 px-4">
        <div className="space-y-2 pb-4">
          <AnimatePresence>
            {filteredTasks.map((task) => (
              <TaskItem key={task.id} task={task} />
            ))}
          </AnimatePresence>
          
          {filteredTasks.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <p className="text-sm">No tasks yet</p>
              <p className="text-xs mt-1">Add a task to get started</p>
            </div>
          )}
        </div>
      </ScrollArea>
      
      {getActiveTasks().length > 0 && (
        <div className="border-t p-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Active tasks:</span>
            <span className="font-medium">{getActiveTasks().length}</span>
          </div>
          <div className="flex items-center justify-between text-sm mt-1">
            <span className="text-muted-foreground">Completed today:</span>
            <span className="font-medium">
              {getCompletedTasks().filter(
                (t) => t.completedAt && 
                  new Date(t.completedAt).toDateString() === new Date().toDateString()
              ).length}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}