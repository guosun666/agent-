from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# 创建所需的解析器
str_parser = StrOutputParser()

# 模型创建
model = ChatTongyi(model="qwen3-max", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

# 第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字。"
)

# 第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

func_lambda = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# 构建链   （AIMessage("{name: 张若曦}")
chain = first_prompt | model | func_lambda | second_prompt | model | str_parser

res = chain.stream({"lastname": "张", "gender": "女儿"})

for chunk in res:
    print(chunk,end="",flush=True)
