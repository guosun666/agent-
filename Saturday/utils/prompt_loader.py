"""
将提示词从txt文件当中取出，并返回文本中的内容字符串。
"""


from utils.path_tool import get_abs_path
from utils.config_handler import prompts_conf
from utils.logger_handler import logger


#except Exception是捕获所有异常
#except KeyError是捕获键错误异常
#except FileNotFoundError是捕获文件不存在异常
#except PermissionError是捕获权限错误异常
#except IOError是捕获输入输出错误异常
#except UnicodeError是捕获编码错误异常
#except ValueError是捕获值错误异常
#except TypeError是捕获类型错误异常
#except NameError是捕获名称错误异常
#except AttributeError是捕获属性错误异常

#加载系统提示词
def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置项中没有找到main_prompt_path,请检查配置文件")
        raise e

    try:
        return open(system_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词出错，失败: {str(e)}")
        # 抛出异常
        raise e

#加载RAG总结提示词
def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置项中没有找到rag_summarize_prompt_path,请检查配置文件")
        raise e

    try:
        return open(rag_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错，失败: {str(e)}")
        # 抛出异常
        raise e

#加载报告提示词
def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置项中没有找到report_prompt_path,请检查配置文件")
        raise e

    try:
        return open(report_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告提示词出错，失败: {str(e)}")
        # 抛出异常
        raise e

if __name__ == "__main__":
    print(load_report_prompts())