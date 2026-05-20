"""
Echo Web 服務：CD 練習用。
未來可以把 echo 邏輯換成 llama.cpp 推理，CD 部分完全不變。
"""

from email import message
from multiprocessing.connection import answer_challenge
import os
from pyexpat.errors import messages
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://llamacpp-server:8080/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "Qwen3.5-0.8B")

client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key="not-needed"
)


app = FastAPI(title="Local LLM API Gateway")

class chatRequest(BaseModel):
    message:str


class TextRequest(BaseModel):
    text:str


def ask_llm(system_prompt: str, user_prompt: str):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role":"system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0.3,
        max_tokens=4096
    )
    print("====================================")
    content = response.choices[0].message.content
    # 移除 think 區塊
    if "<think>" in content:
        parts = content.split("</think>")

        if len(parts) > 1:
            content = parts[-1].strip()
        else:
            # 沒有 </think>，暴力取最後一句
            lines = content.splitlines()
            content = lines[-1]
    # return response.choices[0].message.content
    return content

def route_intent(message: str) -> str:
    meeting_keywords = ["會議", "會議紀錄", "逐字稿", "決議", "待辦", "action item"]
    sop_keywords = ["sop", "SOP", "流程", "步驟", "標準作業", "操作流程"]

    if any(k in message for k in meeting_keywords):
        return "meeting"

    if any(k in message for k in sop_keywords):
        return "sop"

    return "chat"

@app.get("/health")
def health():
    return{
        "status": "ok",
        "llm_base_url": LLM_BASE_URL,
        "model": LLM_MODEL
    }


@app.post("/chat")
def chat(req: chatRequest):
    answer = ask_llm(
        system_prompt = "你是一個簡潔、清楚的AI助手。",
        user_prompt = req.message
    )

    return {
        "response": answer
    }


@app.post("/summarize")
def summarize(req: TextRequest):
    answer = ask_llm(
        system_prompt= "你是一個摘要助手，請用條列式整理重點。",
        user_prompt= f'請摘要以下內容: \n\n{req.text}'
    )

    return {
        "summary": answer
    }

@app.post("/extract")
def extract(req: TextRequest):
    answer = ask_llm(
        system_prompt=(
            "你是一個資訊抽取助手。"
            "請從使用者提供的文字中抽取重點。"
            "並盡量用 JSON 格式輸出。"
        ),
        user_prompt=f"請抽取以下文字的重點、待辦事項、負責人與期限：\n\n{req.text}"
    )

    return {
        "result": answer
    }

@app.post("/kitchen/meeting")
def kitchen_meeting(req: TextRequest):
    answer = ask_llm(
        system_prompt="""
        你是整理會議記錄的分析助手。
        請從使用者提供的文字中抽取重點。
        條列出重要的部分
        """,
        user_prompt=req.text
    )

    return {
        "meeting_record": answer
    }

@app.post("/kitchen/sop")
def kitchen_sop(req: TextRequest):

    answer = ask_llm(
        system_prompt="""
        你是餐飲 SOP 助手。
        請將使用者輸入內容整理成 SOP 步驟。
        只用條列式輸出
        """,
        user_prompt=req.text
    )

    return {
        "sop": answer
    }


@app.post("/kitchen/assistant")
def kitchen_assistant(req: chatRequest):
    intent = route_intent(req.message)

    if intent == "meeting":
        answer = ask_llm(
            system_prompt="""
            你是 AI 廚房會議紀錄助手。
            請將輸入內容整理成：
            1. 會議重點
            2. 決議事項
            3. 待辦事項
            4. 風險與後續追蹤
            """,
            user_prompt=req.message
        )

    elif intent == "sop":
        answer = ask_llm(
            system_prompt="""
            你是 AI 廚房 SOP 助手。
            請將使用者輸入整理成標準作業流程。
            輸出格式：
            1. 作業目的
            2. 前置準備
            3. 操作步驟
            4. 注意事項
            5. 異常處理
            """,
            user_prompt=req.message
        )

    else:
        answer = ask_llm(
            system_prompt="你是 AI 廚房助理，請用清楚、實用的方式回答問題。",
            user_prompt=req.message
        )

    return {
        "intent": intent,
        "response": answer
    }
