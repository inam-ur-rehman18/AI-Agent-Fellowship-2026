"""
AI Workspace — Backend
A small FastAPI service that keeps your Gemini API key on the server
and proxies chat requests to Google's free-tier Gemini API. Also serves
the frontend as static files.

Run it with:  python app.py
"""

import os
from typing import List, Optional

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
# gemini-3.5-flash is on Google's free tier as of mid-2026: free input/output
# tokens within per-model rate limits, no credit card required. Swap via .env
# if Google renames/retires it.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "8192"))
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

app = FastAPI(title="AI Workspace API")

# Wide-open CORS for local development. Tighten this before deploying anywhere public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    system: Optional[str] = None
    model: Optional[str] = None  # UI-facing model label (simulated — see /models)


# The spec calls for a model picker. Only one live model is wired up here;
# the rest are presented for interface parity, same as the in-browser version.
SIMULATED_MODELS = [
    {"id": "gemini", "label": "Gemini", "live": True},
    {"id": "gpt4o-mini", "label": "GPT-4o Mini", "live": False},
    {"id": "gpt4.1", "label": "GPT-4.1", "live": False},
    {"id": "llama", "label": "Llama", "live": False},
    {"id": "claude", "label": "Claude", "live": False},
    {"id": "deepseek", "label": "DeepSeek", "live": False},
]


@app.get("/health")
def health():
    return {"status": "ok", "key_configured": bool(GEMINI_API_KEY), "model": GEMINI_MODEL}


@app.get("/models")
def models():
    return {"models": SIMULATED_MODELS, "active_model": GEMINI_MODEL}


@app.post("/chat")
def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Server is missing GEMINI_API_KEY. Add it to .env and restart the server. "
                   "Get a free key at https://aistudio.google.com/apikey",
        )

    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided.")

    # Gemini uses "user" / "model" roles instead of "user" / "assistant".
    contents = [
        {"role": "model" if m.role == "assistant" else "user", "parts": [{"text": m.content}]}
        for m in req.messages
    ]

    payload = {
        "contents": contents,
        "generationConfig": {"maxOutputTokens": GEMINI_MAX_OUTPUT_TOKENS},
    }
    if req.system:
        payload["system_instruction"] = {"parts": [{"text": req.system}]}

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=60)
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="The request to the AI provider timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Could not reach the AI provider. Check your network connection.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Request to the AI provider failed: {e}")

    if resp.status_code == 401 or resp.status_code == 403:
        raise HTTPException(status_code=401, detail="Invalid or unauthorized Gemini API key.")
    if resp.status_code == 429:
        raise HTTPException(status_code=429, detail="Free-tier rate limit exceeded. Wait a moment and try again.")
    if resp.status_code >= 500:
        raise HTTPException(status_code=502, detail="The AI provider is experiencing issues right now. Please try again shortly.")
    if resp.status_code != 200:
        try:
            detail = resp.json().get("error", {}).get("message", resp.text)
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=400, detail=f"AI provider error: {detail}")

    try:
        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            # Often means the prompt was blocked by safety filters.
            reason = data.get("promptFeedback", {}).get("blockReason")
            if reason:
                raise HTTPException(status_code=400, detail=f"Gemini blocked this request ({reason}). Try rephrasing.")
            raise HTTPException(status_code=502, detail="The AI provider returned no response candidates.")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail="Received an unreadable response from the AI provider.")

    if not text.strip():
        raise HTTPException(status_code=502, detail="The AI provider returned an empty response.")

    return {"content": text, "model": GEMINI_MODEL}


# Serve the frontend. Mounted last so /health, /models, /chat take priority.
_frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
if os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    print("Starting AI Workspace on http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
