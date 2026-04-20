md5_path = "./md5.text"


# chroma（注意：赋值末尾不要随便加逗号，否则会变成元组）
collection_name = "rag"
persist_directory = "./chroma_db"


#splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "","。","！","？"]
max_spilt_char_number = 1000


#retriever
similarity_threshold = 2 #向量检索的相似度阈值

#api_key
api_key = "sk-e90151cacd374f6b865b54c2fe14f1fd"

selected_model = "qwen3-max"


session_config = {"configurable": {"session_id": "user_123"}}