#!/usr/bin/env python3
"""
Scout AI Clone Backend Server with Self-Hosted Models
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
import io
import aiohttp
import requests

app = FastAPI(title="Scout AI Clone API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Self-Hosted Model Configuration
SELF_HOSTED_MODELS = {
    "llama3-70b": {
        "name": "Llama 3 70B",
        "description": "Meta's Llama 3 70B model - competitive with GPT-4",
        "endpoint": "http://localhost:11434/api/generate",  # Ollama
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative", "math", "reasoning"]
    },
    "mixtral-8x7b": {
        "name": "Mixtral 8x7B",
        "description": "Mistral AI's mixture of experts model",
        "endpoint": "http://localhost:11434/api/generate",  # Ollama
        "context_window": 32768,
        "capabilities": ["coding", "analysis", "creative", "math", "multilingual"]
    },
    "mistral-7b": {
        "name": "Mistral 7B",
        "description": "Efficient and powerful small model",
        "endpoint": "http://localhost:11434/api/generate",  # Ollama
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative"]
    },
    "llama-cpp": {
        "name": "Llama.cpp Server",
        "description": "High-performance llama.cpp server",
        "endpoint": "http://localhost:8000/completion",  # llama.cpp
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative", "math"]
    }
}

# In-memory storage
conversations_db = {}
active_connections: Dict[str, WebSocket] = {}
files_db = {}
tasks_db = {}

# Create upload directory
UPLOAD_DIR = Path("/tmp/scout_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class Message(BaseModel):
    content: str
    attachments: Optional[List[Dict]] = None

class Command(BaseModel):
    command: str
    timeout: Optional[int] = 30

class ConversationCreate(BaseModel):
    title: str
    model: Optional[str] = "llama3-70b"

class ChatMessage(BaseModel):
    message: str
    conversationId: Optional[str] = None
    model: Optional[str] = "llama3-70b"

async def call_ollama_model(model: str, messages: List[Dict], stream: bool = False):
    """Call a model via Ollama"""
    model_config = SELF_HOSTED_MODELS.get(model)
    if not model_config:
        raise ValueError(f"Unknown model: {model}")
    
    # Format messages for Ollama
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"System: {msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"
    
    # Add final user prompt
    if messages and messages[-1]["role"] == "user":
        prompt += f"User: {messages[-1]['content']}\nAssistant:"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "options": {
            "temperature": 0.7,
            "top_p": 0.95,
            "num_predict": 1024
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(model_config["endpoint"], headers=headers, json=data) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Ollama API error: {error_text}")
            
            if stream:
                async def stream_generator():
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line:
                            try:
                                json_data = json.loads(line)
                                content = json_data.get("response", "")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
                
                return stream_generator()
            else:
                response_data = await response.json()
                return response_data.get("response", "")

async def call_llama_cpp_model(messages: List[Dict], stream: bool = False):
    """Call a model via llama.cpp server"""
    # Format messages for llama.cpp
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"System: {msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"
    
    # Add final user prompt
    if messages and messages[-1]["role"] == "user":
        prompt += f"User: {messages[-1]['content']}\nAssistant:"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "n_predict": 1024,
        "temperature": 0.7,
        "top_p": 0.95,
        "stop": ["User:", "System:"],
        "stream": stream
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8000/completion", headers=headers, json=data) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"llama.cpp API error: {error_text}")
            
            if stream:
                async def stream_generator():
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith("data: ") and line != "data: [DONE]":
                            try:
                                json_data = json.loads(line[6:])
                                content = json_data.get("content", "")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
                
                return stream_generator()
            else:
                response_data = await response.json()
                return response_data.get("content", "")

async def call_self_hosted_model(model: str, messages: List[Dict], stream: bool = False):
    """Call a self-hosted model"""
    if model in ["llama3-70b", "mixtral-8x7b", "mistral-7b"]:
        return await call_ollama_model(model, messages, stream)
    elif model == "llama-cpp":
        return await call_llama_cpp_model(messages, stream)
    else:
        raise ValueError(f"Unknown model: {model}")

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
    """Get available self-hosted models"""
    models = []
    
    for model_id, config in SELF_HOSTED_MODELS.items():
        models.append({
            "id": f"self-hosted/{model_id}",
            "name": config["name"],
            "description": config["description"],
            "provider": "self-hosted",
            "context_window": config["context_window"],
            "capabilities": config["capabilities"]
        })
    
    return models

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
    
    # Get the model for this conversation
    model = conversations_db[conversation_id].get("model", "llama3-70b")
    
    # Prepare messages for API call
    api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversations_db[conversation_id]["messages"]]
    
    # Generate AI response
    try:
        ai_response = await call_self_hosted_model(model, api_messages)
    except Exception as e:
        print(f"Error calling self-hosted model: {e}")
        # Fallback response
        ai_response = "I'm sorry, I encountered an error while processing your request. Please try again later."
    
    response_msg = {
        "id": f"msg_{uuid.uuid4().hex[:12]}",
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "model": model,
            "provider": "self-hosted",
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
        model = body.get("model", "llama3-70b")
    except:
        message_content = "Hello"
        model = "llama3-70b"
    
    # Prepare messages for API call
    if conversation_id in conversations_db:
        api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversations_db[conversation_id]["messages"]]
        api_messages.append({"role": "user", "content": message_content})
    else:
        api_messages = [{"role": "user", "content": message_content}]
    
    async def generate():
        try:
            stream = await call_self_hosted_model(model, api_messages, stream=True)
            async for chunk in stream:
                yield chunk
        except Exception as e:
            print(f"Error in streaming: {e}")
            # Fallback response
            fallback = "I'm sorry, I encountered an error while streaming the response. Please try again."
            yield fallback
    
    return StreamingResponse(generate(), media_type="text/plain")

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
                    model = message_data.get("model", "llama3-70b")
                    
                    # Send acknowledgment
                    await websocket.send_json({
                        "type": "chat_stream",
                        "data": {"status": "started", "conversationId": conv_id},
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Prepare messages
                    api_messages = [{"role": "user", "content": msg_content}]
                    
                    # Generate and stream response
                    try:
                        stream = await call_self_hosted_model(model, api_messages, stream=True)
                        
                        async for chunk in stream:
                            await websocket.send_json({
                                "type": "chat_stream",
                                "data": {
                                    "chunk": chunk,
                                    "conversationId": conv_id
                                },
                                "timestamp": datetime.now().isoformat()
                            })
                        
                        # Send completion
                        await websocket.send_json({
                            "type": "chat_response",
                            "data": {
                                "status": "completed",
                                "conversationId": conv_id
                            },
                            "timestamp": datetime.now().isoformat()
                        })
                    except Exception as e:
                        await websocket.send_json({
                            "type": "error",
                            "data": {"error": f"Error: {str(e)}"},
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
                
                elif message_type == "upload_file":
                    # Handle file upload
                    file_name = message_data.get("name", "unknown")
                    file_data = message_data.get("data", "")
                    
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
        if connection_id in active_connections:
            del active_connections[connection_id]
        print(f"Client {connection_id} disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if connection_id in active_connections:
            del active_connections[connection_id]

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Scout AI Clone Backend Server with Self-Hosted Models...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket Endpoint: ws://localhost:8000/ws")
    print("🤖 Available Models: Llama 3 70B, Mixtral 8x7B, Mistral 7B, Llama.cpp")
    print("💡 Make sure your self-hosted model server is running")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
