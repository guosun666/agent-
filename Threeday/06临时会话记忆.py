from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)


#模型
model = ChatTongyi(model="qwen3-max", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")
template = PromptTemplate.from_template(
    "你需要根据会话历史回应用户问题，对话历史：{history},请回答用户的问题：{input}"
)
str_parser = StrOutputParser()
store = {}

def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt

#基础链
base_chain = prompt | print_prompt | model | str_parser

#增强链
enhanced_chain = RunnableWithMessageHistory(
    base_chain,  # 被附加历史消息的 Runnable，通常是 Chain
    get_history,  # 获取历史会话的函数
    input_messages_key="input",  # 用户当前输入在 dict 里的键
    history_messages_key="chat_history"  # 历史消息注入到 dict 里的键
)


if __name__ == "__main__":
    session_config = {
        "configurable": 
        {"session_id": "123"
        }
        }
    print(enhanced_chain.invoke(input={"input":"小明有1只猫"},config=session_config))
    print(enhanced_chain.invoke(input={"input":"小张有2只狗"},config=session_config))
    print(enhanced_chain.invoke(input={"input":"共有几个宠物"},config=session_config))





