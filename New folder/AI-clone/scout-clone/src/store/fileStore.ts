import { create } from 'zustand';
import { FileAttachment, ProjectFile } from '@/types';

interface FileState {
  uploadedFiles: FileAttachment[];
  projectFiles: ProjectFile[];
  uploadQueue: FileAttachment[];
  isUploading: boolean;
  
  addFile: (file: FileAttachment) => void;
  removeFile: (id: string) => void;
  updateFileProgress: (id: string, progress: number) => void;
  updateFileStatus: (id: string, status: FileAttachment['status']) => void;
  
  addToQueue: (file: FileAttachment) => void;
  removeFromQueue: (id: string) => void;
  clearQueue: () => void;
  
  setProjectFiles: (files: ProjectFile[]) => void;
  updateProjectFile: (path: string, updates: Partial<ProjectFile>) => void;
  
  setUploading: (uploading: boolean) => void;
  clearFiles: () => void;
}

export const useFileStore = create<FileState>((set) => ({
  uploadedFiles: [],
  projectFiles: [],
  uploadQueue: [],
  isUploading: false,
  
  addFile: (file) => {
    set((state) => ({
      uploadedFiles: [...state.uploadedFiles, file],
    }));
  },
  
  removeFile: (id) => {
    set((state) => ({
      uploadedFiles: state.uploadedFiles.filter((f) => f.id !== id),
    }));
  },
  
  updateFileProgress: (id, progress) => {
    set((state) => ({
      uploadedFiles: state.uploadedFiles.map((f) =>
        f.id === id ? { ...f, uploadProgress: progress } : f
      ),
    }));
  },
  
  updateFileStatus: (id, status) => {
    set((state) => ({
      uploadedFiles: state.uploadedFiles.map((f) =>
        f.id === id ? { ...f, status } : f
      ),
    }));
  },
  
  addToQueue: (file) => {
    set((state) => ({
      uploadQueue: [...state.uploadQueue, file],
    }));
  },
  
  removeFromQueue: (id) => {
    set((state) => ({
      uploadQueue: state.uploadQueue.filter((f) => f.id !== id),
    }));
  },
  
  clearQueue: () => {
    set({ uploadQueue: [] });
  },
  
  setProjectFiles: (files) => {
    set({ projectFiles: files });
  },
  
  updateProjectFile: (path, updates) => {
    const updateFileRecursively = (files: ProjectFile[]): ProjectFile[] => {
      return files.map((file) => {
        if (file.path === path) {
          return { ...file, ...updates };
        }
        if (file.children) {
          return { ...file, children: updateFileRecursively(file.children) };
        }
        return file;
      });
    };
    
    set((state) => ({
      projectFiles: updateFileRecursively(state.projectFiles),
    }));
  },
  
  setUploading: (uploading) => {
    set({ isUploading: uploading });
  },
  
  clearFiles: () => {
    set({ uploadedFiles: [], uploadQueue: [] });
  },
}));