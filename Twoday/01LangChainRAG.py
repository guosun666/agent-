from langchain_community.llms.tongyi import Tongyi

llm = Tongyi(model="qwen-max", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

res = llm.invoke("你好，我是小明，你是谁？")
print(res)
