from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi


template = ChatPromptTemplate.from_messages([
    ("system","你是一个边塞诗人"),
    MessagesPlaceholder("history"),
    ("human","请再来一首"),
])

history_data = [
    ("human","来一首诗"),
    ("ai","大漠孤烟直，长河落日圆。"),
    ("human","请再来一首"),
    ("ai","春风不度玉门关。"),
]
res = template.invoke({"history":history_data}).to_string()

model = ChatTongyi(model="qwen3-max", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

res1 = model.invoke(res)
print(res1.content)








