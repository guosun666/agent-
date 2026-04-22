from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from utils.config_handler import rag_conf

#作为工厂的抽象类，定义了生成模型和嵌入模型的抽象方法，方便后续子类进行重写实现方法
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        key = rag_conf.get("dashscope_api_key") or rag_conf.get("api_key")
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=key,
        )

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=rag_conf["dashscope_api_key"],
        )

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()

