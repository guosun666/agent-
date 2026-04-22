from typing import List

from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document



class RagSummarizerService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.promot_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.promot_text)
        self.model = chat_model
        self.chain = self._init_chain()
    


    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retrieve_docs(self, query: str) -> List[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        # 我从向量库中检索到的文本片段
        context_docs = self.retrieve_docs(query)

        count = 0
        context =""
        for doc in context_docs:
            count += 1
            context += f"【参考资料{count}】：参考资料：{doc.page_content} |参考元数据：{doc.metadata}\n"
        
        return self.chain.invoke(
            {"input": query, "context": context}
        )

if __name__ == "__main__":
    rag = RagSummarizerService()
    print(rag.rag_summarize("小户型适合哪些扫地机器人"))