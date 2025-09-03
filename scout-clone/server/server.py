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

# Model Configuration
SELF_HOSTED_MODELS = {
    "llama3-70b": {
        "name": "Llama 3 70B",
        "description": "Meta's Llama 3 70B model - competitive with GPT-4",
        "endpoint": "http://localhost:8000/completion",  # llama.cpp server
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative", "math", "reasoning"]
    },
    "mixtral-8x7b": {
        "name": "Mixtral 8x7B",
        "description": "Mistral AI's mixture of experts model",
        "endpoint": "http://localhost:8000/completion",
        "context_window": 32768,
        "capabilities": ["coding", "analysis", "creative", "math", "multilingual"]
    },
    "mistral-7b": {
        "name": "Mistral 7B",
        "description": "Efficient and powerful small model",
        "endpoint": "http://localhost:8000/completion",
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative"]
    },
    "falcon-180b": {
        "name": "Falcon 180B",
        "description": "TII's state-of-the-art 180B parameter model",
        "endpoint": "http://localhost:8000/completion",
        "context_window": 2048,
        "capabilities": ["coding", "analysis", "creative", "math"]
    },
    "vicuna-33b": {
        "name": "Vicuna 33B",
        "description": "Fine-tuned chat model based on Llama",
        "endpoint": "http://localhost:8000/completion",
        "context_window": 2048,
        "capabilities": ["chat", "analysis", "creative"]
    }
}

# Ollama Configuration
OLLAMA_MODELS = {
    "llama3": {
        "name": "Llama 3",
        "description": "Meta's latest Llama 3 model",
        "endpoint": "http://localhost:11434/api/generate",
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative", "math"]
    },
    "mixtral": {
        "name": "Mixtral 8x7B",
        "description": "Mistral AI's mixture of experts model",
        "endpoint": "http://localhost:11434/api/generate",
        "context_window": 32768,
        "capabilities": ["coding", "analysis", "creative", "math"]
    },
    "mistral": {
        "name": "Mistral 7B",
        "description": "Efficient and powerful small model",
        "endpoint": "http://localhost:11434/api/generate",
        "context_window": 8192,
        "capabilities": ["coding", "analysis", "creative"]
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

# AI response templates (keep as fallback)
AI_RESPONSES = {
    # ... (your existing templates)
}

# ... (rest of your existing functions)

async def call_self_hosted_model(model: str, messages: List[Dict], stream: bool = False):
    """Call a self-hosted model via llama.cpp server"""
    model_config = SELF_HOSTED_MODELS.get(model)
    if not model_config:
        raise ValueError(f"Unknown model: {model}")
    
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
        async with session.post(model_config["endpoint"], headers=headers, json=data) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Model API error: {error_text}")
            
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

async def call_ollama_model(model: str, messages: List[Dict], stream: bool = False):
    """Call a model via Ollama"""
    model_config = OLLAMA_MODELS.get(model)
    if not model_config:
        raise ValueError(f"Unknown Ollama model: {model}")
    
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

@app.get("/models")
async def get_models():
    """Get available self-hosted models"""
    models = []
    
    # Add self-hosted models
    for model_id, config in SELF_HOSTED_MODELS.items():
        models.append({
            "id": f"self-hosted/{model_id}",
            "name": config["name"],
            "description": config["description"],
            "provider": "self-hosted",
            "context_window": config["context_window"],
            "capabilities": config["capabilities"]
        })
    
    # Add Ollama models
    for model_id, config in OLLAMA_MODELS.items():
        models.append({
            "id": f"ollama/{model_id}",
            "name": config["name"],
            "description": config["description"],
            "provider": "ollama",
            "context_window": config["context_window"],
            "capabilities": config["capabilities"]
        })
    
    return models

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
    model = conversations_db[conversation_id].get("model", "self-hosted/llama3-70b")
    
    # Parse provider and model name
    if "/" in model:
        provider, model_name = model.split("/", 1)
    else:
        provider = "self-hosted"
        model_name = model
    
    # Prepare messages for API call
    api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversations_db[conversation_id]["messages"]]
    
    # Generate AI response
    try:
        if provider == "self-hosted":
            ai_response = await call_self_hosted_model(model_name, api_messages)
        elif provider == "ollama":
            ai_response = await call_ollama_model(model_name, api_messages)
        else:
            # Fallback to demo response
            ai_response = generate_demo_response(message.content)
    except Exception as e:
        print(f"Error calling model: {e}")
        ai_response = generate_demo_response(message.content)
    
    response_msg = {
        "id": f"msg_{uuid.uuid4().hex[:12]}",
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "model": model,
            "provider": provider,
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
        model = body.get("model", "self-hosted/llama3-70b")
    except:
        message_content = "Hello"
        model = "self-hosted/llama3-70b"
    
    # Parse provider and model name
    if "/" in model:
        provider, model_name = model.split("/", 1)
    else:
        provider = "self-hosted"
        model_name = model
    
    # Prepare messages for API call
    if conversation_id in conversations_db:
        api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversations_db[conversation_id]["messages"]]
        api_messages.append({"role": "user", "content": message_content})
    else:
        api_messages = [{"role": "user", "content": message_content}]
    
    async def generate():
        try:
            if provider == "self-hosted":
                stream = await call_self_hosted_model(model_name, api_messages, stream=True)
            elif provider == "ollama":
                stream = await call_ollama_model(model_name, api_messages, stream=True)
            else:
                # Fallback to demo response
                full_response = generate_demo_response(message_content)
                words = full_response.split()
                for i, word in enumerate(words):
                    yield word + (" " if i < len(words) - 1 else "")
                    await asyncio.sleep(random.uniform(0.01, 0.05))
                return
            
            async for chunk in stream:
                yield chunk
        except Exception as e:
            print(f"Error in streaming: {e}")
            # Fallback to demo response
            full_response = generate_demo_response(message_content)
            words = full_response.split()
            for i, word in enumerate(words):
                yield word + (" " if i < len(words) - 1 else "")
                await asyncio.sleep(random.uniform(0.01, 0.05))
    
    return StreamingResponse(generate(), media_type="text/plain")

# ... (rest of your existing code)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Scout AI Clone Backend Server with Self-Hosted Models...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket Endpoint: ws://localhost:8000/ws")
    print("🤖 Available Models: Self-hosted (Llama 3 70B, Mixtral 8x7B, Mistral 7B, Falcon 180B, Vicuna 33B) and Ollama")
    print("💡 Note: Make sure your self-hosted model server is running")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
