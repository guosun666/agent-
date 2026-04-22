import yaml
"""
YAML是专门写[配置文件]的文本格式，使用时，要求配置文件中的内容必须是键值对的形式
k:v
"""
# 文档的目的是把硬盘中的配置文件读取到内存中写为字典对象，方便后续使用
from utils.path_tool import get_abs_path


def load_rag_config(config_path:str=get_abs_path("config/rag.yml"),encoding:str="utf-8")->dict:
    """
    读取RAG配置文件
    """
    with open(config_path,encoding=encoding) as f:
        # 打开配置文件，读取内容，并转换为字典对象
        # Loader=yaml.FullLoader 是告诉yaml库使用全量加载器，确保所有内容都被正确解析
        # yaml.load () = 把 YAML 文本 → 变成 Python 字典
        return yaml.load(f,Loader=yaml.FullLoader)

def load_chroma_config(config_path:str=get_abs_path("config/chroma.yml"),encoding:str="utf-8")->dict:
    """
    读取Chroma配置文件
    """
    with open(config_path,encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_prompts_config(config_path:str=get_abs_path("config/prompts.yml"),encoding:str="utf-8")->dict:
    """
    读取Prompts配置文件
    """
    with open(config_path,encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_agent_config(config_path:str=get_abs_path("config/agent.yml"),encoding:str="utf-8")->dict:
    """
    读取Agent配置文件
    """
    with open(config_path,encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == "__main__":
    print(rag_conf["chat_model_name"])