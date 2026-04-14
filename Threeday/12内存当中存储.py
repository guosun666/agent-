from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader

#内存当中存储
vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(dashscope_api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",
)
documents = loader.load()

vector_store.add_documents(
    documents=documents,            #被添加的文本
    ids=["id"+str(i) for i in range(len(documents))],      #对于每个document分配一个id 
)

vector_store.delete(ids=["id1","id2"])      #删除id为id1和id2的document

results = vector_store.similarity_search(
    query="Python很简单",
    k=3
    )      #相似度搜索，返回k个最相似的document

print(results)










