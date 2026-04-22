from langgraph.types import Command
from typing import Callable
from langchain_core.messages import ToolMessage
from langchain.agents.middleware import (
    wrap_tool_call,
    before_model,
    dynamic_prompt,
    ModelRequest,
    ToolCallRequest,
    AgentState,
)
from langgraph.runtime import Runtime
from utils.prompt_loader import load_report_prompts, load_system_prompts
from utils.logger_handler import logger


"""
外部调用必 try
用户输入必 try
不确定必 try
不能崩的必 try
"""

# 监测工具调用
@wrap_tool_call
def monitor_tool(
    # 请求的数据封装
    request: ToolCallRequest,
    # 执行的函数本身
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:  # 工具执行的监控
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]执行参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具{request.tool_call['name']}调用失败,错误信息：{str(e)}")
        raise


@before_model
def log_before_model(
    state: AgentState,  # 整个Agent智能体中的状态记录
    runtime: Runtime,  # 记录了整个执行过程中的上下文信息
):  # 在模型执行前执行日志
    msgs = state["messages"]
    logger.info(f"[log before model]即将调用模型，带有{len(msgs)}条消息")
    logger.debug(f"[log before model]{type(msgs[-1]).__name__} | {msgs[-1].content.strip()}")

    return None


@dynamic_prompt  # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):  # 动态切换提示词
    is_report = request.runtime.context.get("report", False)
    if is_report:  # 是报告生成场景，返回报告生成提示词内容
        return load_report_prompts()
    return load_system_prompts()
