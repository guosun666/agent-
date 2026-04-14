from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="./data/Python基础语法.txt",
    encoding="utf-8",
)

documents = loader.load()     #[Document对象]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    #分段的最大字符数
    chunk_overlap=50,  #分段的重叠字符数
    length_function=len, #分段的长度函数，默认是len，也可以是其他函数
    separators=["\n\n", "\n", " ", "","。","！","？"], #分段的分隔符
)

splits = splitter.split_documents(documents)    #将一个Document对象分割为多个Document对象

print(type(splits))
for split in splits:
    print("-"*100)
    print(split)
    print("-"*100)