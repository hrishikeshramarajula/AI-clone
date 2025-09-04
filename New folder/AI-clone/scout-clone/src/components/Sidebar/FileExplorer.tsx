import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useFileStore } from '@/store/fileStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import { 
  Folder,
  FolderOpen,
  File,
  FileText,
  FileCode,
  FileImage,
  FileArchive,
  ChevronRight,
  ChevronDown,
  Search,
  Upload,
  Download,
  Trash2,
  RefreshCw,
  X
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { ProjectFile, FileAttachment } from '@/types';
import { format } from 'date-fns';
import { useFileUpload } from '@/hooks/useFileUpload';
import toast from 'react-hot-toast';

export function FileExplorer() {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  
  const { 
    uploadedFiles, 
    projectFiles, 
    uploadQueue,
    isUploading,
    removeFile,
    clearFiles,
  } = useFileStore();
  
  const { getRootProps, getInputProps, isDragActive } = useFileUpload({
    onUploadComplete: (file) => {
      toast.success(`File uploaded: ${file.name}`);
    },
  });
  
  const toggleFolder = (path: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };
  
  const getFileIcon = (file: ProjectFile | FileAttachment) => {
    if ('type' in file && file.type === 'directory') {
      return expandedFolders.has('path' in file ? file.path : file.id) ? (
        <FolderOpen className="h-4 w-4 text-blue-500" />
      ) : (
        <Folder className="h-4 w-4 text-blue-500" />
      );
    }
    
    const name = 'name' in file ? file.name : '';
    const type = 'type' in file && file.type !== 'file' ? file.type : '';
    
    if (type.startsWith('image/') || name.match(/\.(jpg|jpeg|png|gif|svg|webp)$/i)) {
      return <FileImage className="h-4 w-4 text-green-500" />;
    }
    if (type.includes('code') || name.match(/\.(js|ts|jsx|tsx|py|java|cpp|c|h|css|html|xml|json)$/i)) {
      return <FileCode className="h-4 w-4 text-orange-500" />;
    }
    if (type.includes('zip') || type.includes('archive') || name.match(/\.(zip|tar|gz|rar|7z)$/i)) {
      return <FileArchive className="h-4 w-4 text-purple-500" />;
    }
    if (type.includes('text') || name.match(/\.(txt|md|doc|docx|pdf)$/i)) {
      return <FileText className="h-4 w-4 text-gray-500" />;
    }
    
    return <File className="h-4 w-4 text-gray-400" />;
  };
  
  const renderProjectFile = (file: ProjectFile, depth: number = 0) => {
    const isFolder = file.type === 'directory';
    const isExpanded = expandedFolders.has(file.path);
    const isSelected = selectedFile === file.path;
    
    return (
      <div key={file.path}>
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className={cn(
            'flex items-center gap-2 px-2 py-1 hover:bg-muted rounded cursor-pointer',
            isSelected && 'bg-muted',
            'group'
          )}
          style={{ paddingLeft: `${depth * 12 + 8}px` }}
          onClick={() => {
            if (isFolder) {
              toggleFolder(file.path);
            } else {
              setSelectedFile(file.path);
            }
          }}
        >
          {isFolder && (
            <button
              className="p-0.5 hover:bg-muted-foreground/10 rounded"
              onClick={(e) => {
                e.stopPropagation();
                toggleFolder(file.path);
              }}
            >
              {isExpanded ? (
                <ChevronDown className="h-3 w-3" />
              ) : (
                <ChevronRight className="h-3 w-3" />
              )}
            </button>
          )}
          
          {getFileIcon(file)}
          
          <span className="text-sm flex-1 truncate">{file.name}</span>
          
          {!isFolder && file.size && (
            <span className="text-xs text-muted-foreground opacity-0 group-hover:opacity-100">
              {(file.size / 1024).toFixed(1)} KB
            </span>
          )}
        </motion.div>
        
        {isFolder && isExpanded && file.children && (
          <AnimatePresence>
            {file.children.map((child) => renderProjectFile(child, depth + 1))}
          </AnimatePresence>
        )}
      </div>
    );
  };
  
  const renderUploadedFile = (file: FileAttachment) => {
    return (
      <motion.div
        key={file.id}
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 10 }}
        className="flex items-center gap-2 px-2 py-1 hover:bg-muted rounded group"
      >
        {getFileIcon(file)}
        
        <div className="flex-1 min-w-0">
          <p className="text-sm truncate">{file.name}</p>
          {file.status === 'uploading' && file.uploadProgress !== undefined && (
            <Progress value={file.uploadProgress} className="h-1 mt-1" />
          )}
          {file.status === 'error' && (
            <p className="text-xs text-destructive">Upload failed</p>
          )}
        </div>
        
        <div className="flex gap-1 opacity-0 group-hover:opacity-100">
          <Button
            size="sm"
            variant="ghost"
            className="h-6 w-6 p-0"
            onClick={() => window.open(file.url, '_blank')}
          >
            <Download className="h-3 w-3" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="h-6 w-6 p-0"
            onClick={() => removeFile(file.id)}
          >
            <Trash2 className="h-3 w-3" />
          </Button>
        </div>
      </motion.div>
    );
  };
  
  const filteredProjectFiles = projectFiles.filter((file) =>
    file.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  const filteredUploadedFiles = uploadedFiles.filter((file) =>
    file.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 space-y-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search files..."
            className="pl-9"
          />
        </div>
        
        <div
          {...getRootProps()}
          className={cn(
            'border-2 border-dashed rounded-lg p-4 text-center transition-colors cursor-pointer',
            isDragActive ? 'border-primary bg-primary/5' : 'border-muted-foreground/25 hover:border-muted-foreground/50'
          )}
        >
          <input {...getInputProps()} />
          <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            {isDragActive ? 'Drop files here' : 'Drag & drop or click to upload'}
          </p>
        </div>
      </div>
      
      <ScrollArea className="flex-1 px-2">
        <div className="space-y-4 pb-4">
          {projectFiles.length > 0 && (
            <div className="space-y-1">
              <div className="flex items-center justify-between px-2">
                <p className="text-xs font-medium text-muted-foreground">Project Files</p>
                <Button
                  size="sm"
                  variant="ghost"
                  className="h-5 w-5 p-0"
                  onClick={() => window.location.reload()}
                >
                  <RefreshCw className="h-3 w-3" />
                </Button>
              </div>
              {filteredProjectFiles.map((file) => renderProjectFile(file))}
            </div>
          )}
          
          {uploadQueue.length > 0 && (
            <div className="space-y-1">
              <p className="text-xs font-medium text-muted-foreground px-2">Uploading</p>
              <AnimatePresence>
                {uploadQueue.map((file) => renderUploadedFile(file))}
              </AnimatePresence>
            </div>
          )}
          
          {uploadedFiles.length > 0 && (
            <div className="space-y-1">
              <div className="flex items-center justify-between px-2">
                <p className="text-xs font-medium text-muted-foreground">Uploaded Files</p>
                {uploadedFiles.length > 0 && (
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-5 w-5 p-0"
                    onClick={clearFiles}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                )}
              </div>
              <AnimatePresence>
                {filteredUploadedFiles.map((file) => renderUploadedFile(file))}
              </AnimatePresence>
            </div>
          )}
          
          {projectFiles.length === 0 && uploadedFiles.length === 0 && uploadQueue.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <p className="text-sm">No files yet</p>
              <p className="text-xs mt-1">Upload files to get started</p>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}