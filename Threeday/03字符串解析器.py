from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate


example = PromptTemplate.from_template("请用简洁的回答回答用户的问题：{input}")

parser = StrOutputParser()

model = ChatTongyi(model="qwen3-max", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

chain = example | model | parser

res = chain.invoke({"input":"你好，我是小明，我想学习AI"})
print(res)
print(type(res))