from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader

#Chroma 向量数据库（轻量级的）
vector_store = Chroma(
    collection_name="test",          #为当前向量存储起个名字，类似于数据库的表名称
    embedding_function=DashScopeEmbeddings(dashscope_api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
    #指定嵌入模型
    #指定存储的目录，可以指定一个文件夹，也可以指定一个数据库
    persist_directory="./chroma_db",
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",    #指定数据的来源是哪里
)
documents = loader.load()

#添加文档
vector_store.add_documents(
    documents=documents,            #被添加的文本
    ids=["id"+str(i) for i in range(len(documents))],      #对于每个document分配一个id 
)

#删除文档
vector_store.delete(ids=["id1","id2"])      #删除id为id1和id2的document

#相似度搜索
results = vector_store.similarity_search(
    query="Python很简单",
    k=3,
    filter={"source": "黑马程序员"},    #指定过滤条件,内存库不支持元数据过滤
    )      #相似度搜索，返回k个最相似的document
print(results)










