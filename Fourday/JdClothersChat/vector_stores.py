from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):

    def __init__(self,embedding):
        #嵌入模型的传入
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
            )
    
    def get_retriever(self):
        #检索器
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})
    
if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    res = VectorStoreService(DashScopeEmbeddings(dashscope_api_key=config.api_key)).get_retriever()
    print(res.invoke("我的体重180斤，尺码推荐"))
