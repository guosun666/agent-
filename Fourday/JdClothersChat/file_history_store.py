import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")


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
