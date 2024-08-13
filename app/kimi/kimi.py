from openai import OpenAI

client = OpenAI(
    api_key="MOONSHOT_API_KEY",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)


async def kimi_generate():
    stream = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI "
                        "提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI "
                        "为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
        ],
        temperature=0.3,
        stream=True,  # <-- 注意这里，我们通过设置 stream=True 开启流式输出模式
    )

    for chunk in stream:
        delta = chunk.choices[0].delta  # <-- message 字段被替换成了 delta 字段
        if delta.content:
            yield f"data: {delta.content}\n\n"
