#!/usr/bin/env python3
"""
Scout AI Clone Backend Server
A FastAPI server providing WebSocket and REST API endpoints for the Scout AI interface
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import asyncio
import uuid
from datetime import datetime
import os
import subprocess
import shutil
import base64
import hashlib
import time
import random
from pathlib import Path

app = FastAPI(title="Scout AI Clone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str
    attachments: Optional[List[Dict]] = None

class Command(BaseModel):
    command: str
    timeout: Optional[int] = 30

class ConversationCreate(BaseModel):
    title: str
    model: Optional[str] = "claude-3-opus"

class ChatMessage(BaseModel):
    message: str
    conversationId: Optional[str] = None
    model: Optional[str] = "claude-3-opus"

# In-memory storage
conversations_db = {}
active_connections: Dict[str, WebSocket] = {}
files_db = {}
tasks_db = {}

# Create upload directory
UPLOAD_DIR = Path("/tmp/scout_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# AI response templates for realistic demo
AI_RESPONSES = {
    "greeting": [
        "Hello! I'm Scout, your AI assistant. How can I help you today?",
        "Hi there! I'm ready to assist you with coding, research, or any task you have in mind.",
        "Welcome! I'm Scout, and I'm here to help. What would you like to work on?",
    ],
    "coding": [
        "I'll help you with that code. Let me analyze the requirements and provide a solution.",
        "I understand what you're looking for. Here's my approach to solving this problem:",
        "Great coding question! Let me break this down and provide you with a comprehensive solution.",
    ],
    "research": [
        "I'll research that topic for you. Let me gather relevant information.",
        "That's an interesting topic. Let me compile some comprehensive information for you.",
        "I'll help you explore that subject. Here's what I've found:",
    ],
    "general": [
        "I understand your request. Let me work on that for you.",
        "I'll help you with that. Here's my analysis:",
        "Let me process that information and provide you with a detailed response.",
    ],
}

def get_ai_response_type(message: str) -> str:
    """Determine the type of AI response based on the message content"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "greeting"
    elif any(word in message_lower for word in ["code", "function", "class", "debug", "program", "script"]):
        return "coding"
    elif any(word in message_lower for word in ["research", "find", "search", "information", "learn"]):
        return "research"
    else:
        return "general"

def generate_demo_response(message: str) -> str:
    """Generate a realistic demo response based on the message"""
    response_type = get_ai_response_type(message)
    base_response = random.choice(AI_RESPONSES[response_type])
    
    # Add specific content based on the message
    if "code" in message.lower():
        base_response += "\n\n```python\n# Example implementation\ndef solution():\n    # Your code logic here\n    pass\n```\n\nThis solution provides a clean and efficient approach to your problem."
    elif "explain" in message.lower():
        base_response += "\n\nHere's a detailed explanation:\n\n1. **Concept Overview**: Understanding the fundamental principles\n2. **Implementation Details**: How it works in practice\n3. **Best Practices**: Recommended approaches\n4. **Common Pitfalls**: What to avoid"
    elif "?" in message:
        base_response += f"\n\nTo directly answer your question: {message}\n\nThe solution involves considering multiple factors and implementing a comprehensive approach."
    
    return base_response

@app.get("/")
async def root():
    return {
        "message": "Scout AI Clone API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "/ws",
            "api_docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": len(active_connections),
        "conversations": len(conversations_db)
    }

@app.get("/models")
async def get_models():
    """Get available AI models"""
    return [
        {
            "id": "claude-3-opus",
            "name": "Claude 3 Opus",
            "description": "Most capable model for complex tasks",
            "context_window": 200000,
            "capabilities": ["coding", "analysis", "creative", "math", "vision"]
        },
        {
            "id": "claude-3-sonnet",
            "name": "Claude 3 Sonnet",
            "description": "Balanced performance and speed",
            "context_window": 200000,
            "capabilities": ["coding", "analysis", "creative", "math", "vision"]
        },
        {
            "id": "claude-3-haiku",
            "name": "Claude 3 Haiku",
            "description": "Fastest responses for simple tasks",
            "context_window": 200000,
            "capabilities": ["coding", "analysis", "creative"]
        },
        {
            "id": "gpt-4-turbo",
            "name": "GPT-4 Turbo",
            "description": "Latest GPT-4 with vision",
            "context_window": 128000,
            "capabilities": ["coding", "analysis", "creative", "math", "vision"]
        },
        {
            "id": "gpt-4",
            "name": "GPT-4",
            "description": "Advanced reasoning and analysis",
            "context_window": 8192,
            "capabilities": ["coding", "analysis", "creative", "math"]
        },
        {
            "id": "gpt-3.5-turbo",
            "name": "GPT-3.5 Turbo",
            "description": "Fast and efficient for most tasks",
            "context_window": 16385,
            "capabilities": ["coding", "analysis", "creative"]
        },
    ]

@app.post("/conversations")
async def create_conversation(conversation: ConversationCreate):
    """Create a new conversation"""
    conv_id = f"conv_{uuid.uuid4().hex[:12]}"
    conversations_db[conv_id] = {
        "id": conv_id,
        "title": conversation.title,
        "model": conversation.model,
        "messages": [],
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "metadata": {
            "total_messages": 0,
            "total_tokens": 0
        }
    }
    return conversations_db[conv_id]

@app.get("/conversations")
async def get_conversations():
    """Get all conversations"""
    return list(conversations_db.values())

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversations_db[conversation_id]

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    del conversations_db[conversation_id]
    return {"message": "Conversation deleted successfully"}

@app.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, message: Message):
    """Add a message to a conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Add user message
    user_msg = {
        "id": f"msg_{uuid.uuid4().hex[:12]}",
        "role": "user",
        "content": message.content,
        "attachments": message.attachments,
        "timestamp": datetime.now().isoformat(),
    }
    
    conversations_db[conversation_id]["messages"].append(user_msg)
    conversations_db[conversation_id]["updatedAt"] = datetime.now().isoformat()
    conversations_db[conversation_id]["metadata"]["total_messages"] += 1
    
    # Generate AI response
    ai_response = generate_demo_response(message.content)
    
    response_msg = {
        "id": f"msg_{uuid.uuid4().hex[:12]}",
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "model": conversations_db[conversation_id].get("model", "claude-3-opus"),
            "tokens_used": len(ai_response.split()),
            "execution_time": random.uniform(0.5, 2.0)
        }
    }
    conversations_db[conversation_id]["messages"].append(response_msg)
    conversations_db[conversation_id]["metadata"]["total_messages"] += 1
    
    return response_msg

@app.post("/conversations/{conversation_id}/stream")
async def stream_chat(conversation_id: str, request: Request):
    """Stream a chat response"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        body = await request.json()
        message_content = body.get("message", "")
    except:
        message_content = "Hello"
    
    async def generate():
        # Generate a realistic response
        full_response = generate_demo_response(message_content)
        
        # Simulate streaming by sending chunks
        words = full_response.split()
        for i, word in enumerate(words):
            # Send word with space
            yield word + (" " if i < len(words) - 1 else "")
            # Simulate processing time
            await asyncio.sleep(random.uniform(0.01, 0.05))
    
    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/bash")
async def execute_bash(command: Command):
    """Execute a bash command (sandboxed for demo)"""
    # For security, only allow certain safe commands in demo
    safe_commands = ["ls", "pwd", "date", "echo", "cat", "head", "tail", "wc"]
    cmd_parts = command.command.split()
    
    if not cmd_parts or cmd_parts[0] not in safe_commands:
        return {
            "output": f"Command '{cmd_parts[0] if cmd_parts else ''}' is not allowed in demo mode",
            "error": "Only safe commands are allowed: " + ", ".join(safe_commands),
            "exitCode": 1
        }
    
    try:
        result = subprocess.run(
            command.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=command.timeout,
            cwd="/tmp"
        )
        return {
            "output": result.stdout,
            "error": result.stderr,
            "exitCode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": "Command timed out",
            "exitCode": -1
        }
    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "exitCode": -1
        }

@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file"""
    file_id = f"file_{uuid.uuid4().hex[:12]}"
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    
    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Calculate file hash
    file_hash = hashlib.md5(content).hexdigest()
    
    # Store file metadata
    files_db[file_id] = {
        "id": file_id,
        "name": file.filename,
        "size": len(content),
        "type": file.content_type,
        "path": str(file_path),
        "hash": file_hash,
        "uploaded_at": datetime.now().isoformat(),
        "url": f"/files/{file_id}/download",
        "status": "uploaded"
    }
    
    return files_db[file_id]

@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    """Download a file"""
    if file_id not in files_db:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = files_db[file_id]
    file_path = Path(file_info["path"])
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    with open(file_path, "rb") as f:
        content = f.read()
    
    return StreamingResponse(
        io.BytesIO(content),
        media_type=file_info.get("type", "application/octet-stream"),
        headers={
            "Content-Disposition": f'attachment; filename="{file_info["name"]}"'
        }
    )

@app.get("/files")
async def list_files():
    """List all uploaded files"""
    return list(files_db.values())

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete a file"""
    if file_id not in files_db:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = files_db[file_id]
    file_path = Path(file_info["path"])
    
    if file_path.exists():
        file_path.unlink()
    
    del files_db[file_id]
    return {"message": "File deleted successfully"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    connection_id = f"conn_{uuid.uuid4().hex[:12]}"
    active_connections[connection_id] = websocket
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "data": {
                "connectionId": connection_id,
                "message": "Connected to Scout AI Clone"
            },
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type", "")
                message_data = message.get("data", {})
                
                # Handle different message types
                if message_type == "ping":
                    # Respond to ping with pong
                    await websocket.send_json({
                        "type": "pong",
                        "data": {"timestamp": message_data.get("timestamp")},
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif message_type == "chat_message":
                    # Handle chat message
                    conv_id = message_data.get("conversationId")
                    msg_content = message_data.get("message", "")
                    
                    # Send acknowledgment
                    await websocket.send_json({
                        "type": "chat_stream",
                        "data": {"status": "started", "conversationId": conv_id},
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Generate and stream response
                    response = generate_demo_response(msg_content)
                    words = response.split()
                    
                    for i, word in enumerate(words):
                        await websocket.send_json({
                            "type": "chat_stream",
                            "data": {
                                "chunk": word + (" " if i < len(words) - 1 else ""),
                                "conversationId": conv_id
                            },
                            "timestamp": datetime.now().isoformat()
                        })
                        await asyncio.sleep(0.03)
                    
                    # Send completion
                    await websocket.send_json({
                        "type": "chat_response",
                        "data": {
                            "status": "completed",
                            "conversationId": conv_id,
                            "fullResponse": response
                        },
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif message_type == "execute_command":
                    # Execute command
                    command = message_data.get("command", "")
                    
                    await websocket.send_json({
                        "type": "command_output",
                        "data": {"output": f"Executing: {command}"},
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Simulate command execution
                    await asyncio.sleep(1)
                    
                    await websocket.send_json({
                        "type": "command_complete",
                        "data": {
                            "output": f"Command '{command}' executed successfully",
                            "exitCode": 0
                        },
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif message_type == "tool_call":
                    # Handle tool call
                    tool_name = message_data.get("name", "unknown")
                    tool_args = message_data.get("arguments", {})
                    
                    # Send running status
                    await websocket.send_json({
                        "type": "tool_call",
                        "data": {
                            "name": tool_name,
                            "description": f"Executing {tool_name}",
                            "status": "running",
                            "arguments": tool_args
                        },
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Simulate tool execution
                    await asyncio.sleep(random.uniform(0.5, 2))
                    
                    # Send completion
                    await websocket.send_json({
                        "type": "tool_call",
                        "data": {
                            "name": tool_name,
                            "description": f"Completed {tool_name}",
                            "status": "completed",
                            "result": {
                                "success": True,
                                "output": f"{tool_name} executed successfully"
                            }
                        },
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif message_type == "upload_file":
                    # Handle file upload via WebSocket
                    file_name = message_data.get("name", "unknown")
                    file_data = message_data.get("data", "")
                    
                    # Decode base64 data
                    try:
                        file_bytes = base64.b64decode(file_data)
                        file_id = f"file_{uuid.uuid4().hex[:12]}"
                        file_path = UPLOAD_DIR / f"{file_id}_{file_name}"
                        
                        with open(file_path, "wb") as f:
                            f.write(file_bytes)
                        
                        await websocket.send_json({
                            "type": "file_uploaded",
                            "data": {
                                "id": file_id,
                                "name": file_name,
                                "size": len(file_bytes),
                                "status": "uploaded"
                            },
                            "timestamp": datetime.now().isoformat()
                        })
                    except Exception as e:
                        await websocket.send_json({
                            "type": "error",
                            "data": {"error": f"File upload failed: {str(e)}"},
                            "timestamp": datetime.now().isoformat()
                        })
                
                else:
                    # Echo unknown messages
                    await websocket.send_json({
                        "type": "echo",
                        "data": message_data,
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "data": {"error": "Invalid JSON format"},
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "data": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                })
                
    except WebSocketDisconnect:
        del active_connections[connection_id]
        print(f"Client {connection_id} disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if connection_id in active_connections:
            del active_connections[connection_id]

# Tasks API endpoints
@app.post("/tasks")
async def create_task(task: Dict[str, Any]):
    """Create a new task"""
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    tasks_db[task_id] = {
        "id": task_id,
        "title": task.get("title", "Untitled Task"),
        "description": task.get("description", ""),
        "status": "pending",
        "progress": 0,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    return tasks_db[task_id]

@app.get("/tasks")
async def get_tasks():
    """Get all tasks"""
    return list(tasks_db.values())

@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, updates: Dict[str, Any]):
    """Update a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_db[task_id].update(updates)
    tasks_db[task_id]["updatedAt"] = datetime.now().isoformat()
    
    # Notify connected clients
    for ws in active_connections.values():
        try:
            await ws.send_json({
                "type": "task_update",
                "data": tasks_db[task_id],
                "timestamp": datetime.now().isoformat()
            })
        except:
            pass
    
    return tasks_db[task_id]

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    import io
    
    print("🚀 Starting Scout AI Clone Backend Server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket Endpoint: ws://localhost:8000/ws")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)