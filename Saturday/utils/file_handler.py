import os 
import hashlib
from logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

#获取文件的md5的十六进制字符串
def get_file_md5_hex(filepath:str):
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]{filepath} 文件路径不正确")
        return 
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]{filepath} 不是文件")
        return
    #创建md5对象
    md5_obj = hashlib.md5()

    chunk_size = 4096 # 4KB分片，避免文件过大爆内存
    try:
        with open(filepath,'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            """
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath} md5计算失败: {str(e)}")
        return None


#查看文件夹下的文件的类型是否符合allowed_types
def listdir_with_allowed_type(path:str,allowed_types:tuple[str]):
    files = []
    # 如果文件夹不存在,则返回空列表
    if not os.path.exists(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types

    #遍历文件夹下的文件,如果文件的类型符合allowed_types,则将文件添加到files列表中
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))
    return tuple(files)

#加载pdf文件,返回类型是list[Document]
def pdf_loader(filepath:str,passwd=None):
    return PyPDFLoader(filepath,password=passwd).load()

#加载txt文件,返回类型是list[Document]
def txt_loader(filepath:str):
    return TextLoader(filepath).load()