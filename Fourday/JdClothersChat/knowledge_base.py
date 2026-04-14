import os
import config_data as config
import hashlib
from typing import List
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
#用来检查传入的md5字符串是否已经被处理过了，return False(md5未被处理)  True(md5已处理)
def check_md5(md5_str):
    #if进入表示文件不存在，那肯定没有处理过这个md5
    if not os.path.exists(config.md5_path):
        #创建文件
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        #文件存在，读取文件内容
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()    #处理字符串前后的空格和回车
            if line == md5_str:
                return True
        #如果遍历完了，没有找到，则返回False，或者是内容是空，readlines是返回一个空列表，则返回False
        return False


def save_md5(md5_str):
    #将传入的md5字符串写入文件
    #用 with 语法，自动管理「进入时做什么，退出时做什么」
    # 进入时：打开文件 =====> 自动调用 f.open()方法
    # 退出时：关闭文件 =====> 自动调用 f.close()方法
    with open(config.md5_path, "a", encoding="utf-8") as f:
        # 写入文件
        f.write(md5_str + "\n")

def get_string_md5(input_str,encoding="utf-8"):
    #将字符串转换为md5的输入字节流
    str_bytes= input_str.encode(encoding=encoding)
    #创建md5对象
    md5_obj = hashlib.md5()
    #更新md5对象
    md5_obj.update(str_bytes)
    #返回md5字符串
    return md5_obj.hexdigest()

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(dashscope_api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
            persist_directory=config.persist_directory
        ) #向量存储的实例 Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,      #分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,  #分割后的文本段重叠长度
            separators=config.separators,  #分割后的文本段分隔符
            length_function=len,  #默认用len函数计算文本段长度
            )    #文本切分的实例，TextSplitter对象
    
    def upload_by_str(self,data,filename):
    #将传入的字符串，进行向量化，存入向量数据库中
    #先看它在不在数据库当中，在的话，跳过，不在的话，
    #进行分割（长文本就分割，短文本就原封不动），然后存入数据库
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        if len(data) > config.max_spilt_char_number:
            knowledeg_chunks:List[str] = self.spliter.split_text(data)
        else:
            knowledeg_chunks = [data]
        
        doc_metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小曹",
        }

        self.chroma.add_texts(
            texts=knowledeg_chunks,
            metadatas=[doc_metadata for _ in knowledeg_chunks],
        )
        save_md5(md5_hex)

        return "[成功]内容已存入知识库中"
 

if __name__ == "__main__":
    knowledge_base_service = KnowledgeBaseService()
    print(knowledge_base_service.upload_by_str("周杰伦", "testfile"))



