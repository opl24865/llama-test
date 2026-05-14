from openai import OpenAI

client = OpenAI(
    base_url="http://llamacpp-server:8080/v1",
    api_key="dummy"
)

response = client.chat.completions.create(
    model="Qwen3.5-0.8B-Q8_0.gguf",
    messages=[
        {
            "role": "user",
            "content": "你好"
        }
    ]
)

print(response.choices[0].message.content)
