import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { apiService } from '@/services/api';
import { useFileStore } from '@/store/fileStore';
import { FileAttachment } from '@/types';
import toast from 'react-hot-toast';

interface UseFileUploadOptions {
  maxSize?: number;
  maxFiles?: number;
  accept?: Record<string, string[]>;
  onUploadComplete?: (file: FileAttachment) => void;
  onUploadError?: (error: Error) => void;
}

export function useFileUpload(options: UseFileUploadOptions = {}) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<Record<string, number>>({});
  const { addFile, updateFileProgress, updateFileStatus } = useFileStore();
  
  const uploadFile = useCallback(
    async (file: File) => {
      const fileId = `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      const fileAttachment: FileAttachment = {
        id: fileId,
        name: file.name,
        size: file.size,
        type: file.type,
        url: URL.createObjectURL(file),
        status: 'uploading',
        uploadProgress: 0,
      };
      
      addFile(fileAttachment);
      setIsUploading(true);
      
      try {
        const uploadedFile = await apiService.uploadFile(file, (progress) => {
          setUploadProgress((prev) => ({ ...prev, [fileId]: progress }));
          updateFileProgress(fileId, progress);
        });
        
        updateFileStatus(fileId, 'uploaded');
        options.onUploadComplete?.(uploadedFile);
        toast.success(`File "${file.name}" uploaded successfully`);
        
        return uploadedFile;
      } catch (error) {
        updateFileStatus(fileId, 'error');
        const errorMessage = error instanceof Error ? error.message : 'Upload failed';
        toast.error(`Failed to upload "${file.name}": ${errorMessage}`);
        options.onUploadError?.(error instanceof Error ? error : new Error(errorMessage));
        throw error;
      } finally {
        setIsUploading(false);
        setUploadProgress((prev) => {
          const { [fileId]: _, ...rest } = prev;
          return rest;
        });
      }
    },
    [addFile, updateFileProgress, updateFileStatus, options]
  );
  
  const uploadMultiple = useCallback(
    async (files: File[]) => {
      const results = await Promise.allSettled(files.map(uploadFile));
      
      const successful = results.filter(
        (r): r is PromiseFulfilledResult<FileAttachment> => r.status === 'fulfilled'
      );
      
      const failed = results.filter(
        (r): r is PromiseRejectedResult => r.status === 'rejected'
      );
      
      if (failed.length > 0) {
        toast.error(`${failed.length} file(s) failed to upload`);
      }
      
      return successful.map((r) => r.value);
    },
    [uploadFile]
  );
  
  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (options.maxFiles && acceptedFiles.length > options.maxFiles) {
        toast.error(`Maximum ${options.maxFiles} files allowed`);
        return;
      }
      
      await uploadMultiple(acceptedFiles);
    },
    [uploadMultiple, options.maxFiles]
  );
  
  const dropzone = useDropzone({
    onDrop,
    maxSize: options.maxSize,
    accept: options.accept,
    multiple: true,
  });
  
  return {
    ...dropzone,
    uploadFile,
    uploadMultiple,
    isUploading,
    uploadProgress,
  };
}