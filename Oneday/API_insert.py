from openai import OpenAI
#获取client对象，通过url_base指定api地址
client = OpenAI(
    api_key="sk-e90151cacd374f6b865b54c2fe14f1fd",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role":"system","content":"你是一个前端专家，简洁回答问题"},
        {"role":"assistant","content":"你好，你有什么问题来问我"},
        {"role":"user","content":"我想学习前端，你有什么推荐吗？"}],
        stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content,end="",flush=True)
