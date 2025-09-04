# server/server.py (add/replace in your FastAPI app)

import os
from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()  # Loads .env

app = FastAPI(title="Scout AI Clone API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load search API keys from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
DUCKDUCKGO_API_KEY = os.getenv("DUCKDUCKGO_API_KEY")
BING_API_KEY = os.getenv("BING_SEARCH_API_KEY")

class SearchRequest(BaseModel):
    query: str
    engine: str  # "google", "duckduckgo", "bing"

class SearchResult(BaseModel):
    title: str
    snippet: str
    url: str

@app.post("/search", response_model=list[SearchResult])
async def search(request: SearchRequest):
    """
    Search endpoint supporting google, duckduckgo, or bing.
    """
    engine = request.engine.lower()
    query = request.query
    headers = {"Content-Type": "application/json"}
    params = {}
    url = ""

    if engine == "google":
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"key": GOOGLE_API_KEY, "cx": os.getenv("GOOGLE_CX"), "q": query}
    elif engine == "duckduckgo":
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "api_key": DUCKDUCKGO_API_KEY}
    elif engine == "bing":
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers["Ocp-Apim-Subscription-Key"] = BING_API_KEY
        params = {"q": query, "count": 5}
    else:
        raise HTTPException(status_code=400, detail="Unsupported search engine")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise HTTPException(status_code=500, detail=f"Search API error: {text}")
            data = await resp.json()

    results = []
    if engine == "google":
        for item in data.get("items", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    url=item.get("link", "")
                )
            )
    elif engine == "duckduckgo":
        for topic in data.get("RelatedTopics", []):
            if "Text" in topic and "FirstURL" in topic:
                results.append(
                    SearchResult(
                        title=topic["Text"],
                        snippet=topic["Text"],
                        url=topic["FirstURL"]
                    )
                )
    else:  # bing
        for item in data.get("webPages", {}).get("value", []):
            results.append(
                SearchResult(
                    title=item.get("name", ""),
                    snippet=item.get("snippet", ""),
                    url=item.get("url", "")
                )
            )

    return results

# WebSocket tool_call for search
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    conn_id = f"conn_{uuid.uuid4().hex[:12]}"
    await ws.send_json({"type": "connected", "data": {"connectionId": conn_id}})
    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("type") == "tool_call" and msg["data"].get("tool") == "search":
                engine = msg["data"].get("engine")
                query = msg["data"].get("query")
                # Call the HTTP search endpoint internally
                search_req = SearchRequest(query=query, engine=engine)
                results = await search(search_req)
                await ws.send_json({
                    "type": "tool_response",
                    "data": {"tool": "search", "results": [r.dict() for r in results]}
                })
            else:
                # pass other message types to existing handlers
                pass
    except WebSocketDisconnect:
        return
