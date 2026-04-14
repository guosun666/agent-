md5_path = "./md5.text"


# chroma（注意：赋值末尾不要随便加逗号，否则会变成元组）
collection_name = "rag"
persist_directory = "./chroma_db"


#splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "","。","！","？"]
max_spilt_char_number = 1000
