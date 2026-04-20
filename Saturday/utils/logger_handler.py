import logging
from path_tool import get_abs_path
import os
from datetime import datetime


# 日志的根目录
LOG_ROOT = get_abs_path("logs")

# 确保日志的目录存在
os.makedirs(LOG_ROOT,exist_ok=True)

# 日志的格式配置 ：error info debug

# 创建时间、日志名称、日志级别、文件名、行号、日志内容
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

"""(数字越小，级别越高，大于它的级别都会被记录)
DEBUG (10)   👉 调试细节（最详细）
INFO  (20)   👉 普通信息
WARNING (30) 👉 警告
ERROR (40)   👉 错误
CRITICAL(50)👉 严重错误
"""
"""
          ┌──→ 控制台处理器 (StreamHandler) → 屏幕输出
Logger ───┤
          └──→ 文件处理器 (FileHandler)     → 写入文件
"""


# 创建日志记录器
def get_logger(
    name:str = "agent", # 日志的名字
    console_level: int = logging.INFO,    # 控制台的日志级别(背后是int类型)
    file_level: int = logging.DEBUG,    # 文件的日志级别(背后是int类型)
    log_file = None,  
    ) -> logging.Logger:        # 返回日志记录器(Logger)—— logging 模块里的 Logger 对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 如果logger已经有处理器，则直接返回logger，防止重复添加处理器
    if logger.handlers:
        return logger

    #控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    #文件处理器

    # 如果log_file为空，则创建一个日志文件
    if not log_file:
        log_file = os.path.join(LOG_ROOT,f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # datetime.now()得到的返回类型是时间对象，.strftime('%Y-%m-%d') 是将时间对象转换为字符串，格式为：2026-04-20

    file_handler = logging.FileHandler(log_file,encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

#快捷获取日志器
logger = get_logger()

if __name__ == "__main__":
    logger.info("这是一个测试日志")
    logger.warning("这是一个警告日志")
    logger.error("这是一个错误日志")
    logger.debug("这是一个调试日志")