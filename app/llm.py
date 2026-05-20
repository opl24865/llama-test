import os
from openai import OpenAI


LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://llamacpp-server:8080/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "Qwen2.5-1.5B-Instruct")


client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key="not-needed"
)


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3,
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