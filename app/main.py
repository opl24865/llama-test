from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel

from app.llm import ask_llm
from app.router import route_intent
from app.prompts import get_prompt


app = FastAPI(title="AI Kitchen LLM Gateway")

class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def healhth():
    return{
        "status": "ok",
        "service": "AI Kitchen LLM Gateway"
    }

@app.get("/", response_class=HTMLResponse)
def home():
    html_path = Path("app/templates/index.html")
    return html_path.read_text(encoding="utf-8")

@app.post("/kitchen/assistant")
def kitchen_assistant(req: ChatRequest):
    intent = route_intent(req.message)
    system_prompt = get_prompt(intent)

    answer = ask_llm(
        system_prompt=system_prompt,
        user_prompt=req.message
    )

    return {
        "intent": intent,
        "response": answer
    }

@app.post("/chat")
def chat(req: ChatRequest):
    answer = ask_llm(
        system_prompt=get_prompt("general"),
        user_prompt=req.message
    )

    return {
        "response": answer
    }