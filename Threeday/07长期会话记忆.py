import json
import os
from typing import Sequence
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id    #会话id
        self.storage_path = storage_path  #存储路径
        
        self.file_path = os.path.join(self.storage_path,self.session_id)  #文件路径
        
        #确保文件夹是存在的，如果不存在则创建
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    #Sequence序列 类似于list，tuple
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:

        all_messages = list(self.messages)      #确保兼容性Sequence[BaseMessage]转换为List[BaseMessage]，已有的消息列表
        all_messages.extend(messages)           #添加新消息
        
        #将数据同步写到本地文件当中   类对象写到文件当中是二进制，可以将BaseMessage消息转为字典
        # new_messages = []
        # for message in all_messages:
        #     d = message.to_dict(message)
        #     new_messages.append(d)
        new_messages = [message_to_dict(message) for message in all_messages]
        #字典序列化成json格式
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages,f)
    @property          #通过property装饰器，将messages方法变成属性，可以直接通过类对象.messages访问
    def messages(self) -> list[BaseMessage]:
        #带 s = 处理字符串（loads / dumps）
        # 不带 s = 处理文件（load / dump）
        #当前文件内:是List[Json],然后load之后返回的是List[Dict],为了转换为消息对象，使用messages_from_dict
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                messages_data = json.load(f)       
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
    
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)









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

def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")



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
    # print(enhanced_chain.invoke(input={"input":"小明有1只猫"},config=session_config))
    # print(enhanced_chain.invoke(input={"input":"小张有2只狗"},config=session_config))
    print(enhanced_chain.invoke(input={"input":"共有几个宠物"},config=session_config))





