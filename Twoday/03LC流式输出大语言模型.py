from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-turbo", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

res = model.stream(input="你好，我是小明，你是谁？")

for chunk in res:
    print(chunk,end="",flush=True)