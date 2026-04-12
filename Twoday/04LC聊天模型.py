from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

model = ChatTongyi(model="qwen3-max", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

messages = [
    #是静态的，直接得到了Message类的类对象
    SystemMessage(content="你是一个边塞诗人"),
    HumanMessage(content="写一首关于边塞的诗"),
    AIMessage(content="大漠孤烟直，长河落日圆。"),
    HumanMessage(content="按照这个诗的格式，写一首关于边塞的诗"),
'''简写形式 是动态的，需要在运行时由LangChain内部机制为Message类对象（简写时支持变量的占位符）
messages = [
    ("system","你是一个边塞诗人"),
    ("human","写一首关于边塞的诗"),
    ("ai","大漠孤烟直，长河落日圆。"),
    ("human","按照这个诗的格式，写一首关于边塞的诗"),
    ]
'''
]

res =model.stream(input=messages)
#.content是获取chunk中的内容
for chunk in res:
    print(chunk.content,end="",flush=True)

