from openai import OpenAI
import time
client = OpenAI(
    base_url="http://llamacpp-server:8080/v1",
    api_key="dummy"
)


while True:
    try:

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
        break
    
    except Exception as e:
        print("Model loading, retrying...")
        print(e)
        time.sleep(5)

