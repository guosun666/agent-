"""
它的作用是加载一个向量库类。
1 在这个类当中初始化向量库和分词器，方便后期更换参数，我们将参数放到对应的yaml的文件当中去进行管理，然后调用config_handler类去调用方法去进行引用。
2 对于向量库，我们关键要进行检索。这里多实现的一个功能是加载文档。
3 它不是直接拿到文件路径然后直接加载的，而是从调用file_handler类的方法去从文件夹当中筛选出符合配置文件要求的文件，
  并对于每个文件调用将文件唯一标识的md5值的方法，如果没有值不执行，有值判断知识库有没有，有跳出，没用则将文件加载，然后分片存入向量库当中去，再保存。
"""


from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
import os

#加载向量库
class VectorStoreService:
    # 初始化向量库和分词器
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )
    # 获取检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    # 加载文档
    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """

        # 检查文件的MD5是否已经处理过
        def check_md5_hex(md5_for_check: str):
            # 检查文件是否存在
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False            
            # 检查文件是否已经处理过
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True     # md5 处理过

                return False            # md5 没处理过

        
        # 将处理成功的文件MD5写入记录文件
        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")
        
        # 根据文件的后缀调用不同的加载器，返回值都是List[Document]
        def get_file_documents(read_path: str):
            p = read_path.lower()
            if p.endswith(".txt"):
                return txt_loader(read_path)
            if p.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        # 从文件夹里面找到符合的文件路径放到列表当中去，返回值是tuple[str]
        allowed_files_path = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_types"]),
        )
        # 遍历允许的文件路径
        for path in allowed_files_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)
            # 如果md5_hex为空文件，则跳过
            if not md5_hex:
                continue
            #已经是文件，而且有md5值，接下来判断有没有在知识库当中
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue



if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)



