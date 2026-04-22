from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, fetch_external_data, fill_context_for_report
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )
    
    def execute_stream(self, query: str):
        input_dict={
            "messages":[
                {"role":"user","content":query}
            ]
        }
        # stream_mode="values" 是流式输出的模式，返回的是值，而不是消息
        # 第三个参数context就是上下文runtime中的信息，就是我们做提示词切换的标记
        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

"""
第1条：HumanMessage用户消息:扫地机器人在我所在的地区的气温下如何保养
(调用get_user_location工具，返回用户所在地区)
第2条：AIMessage AI思考消息
第3条：ToolMessage工具返回结果消息: 深圳
(调用get_weather工具，返回用户所在地区的气温)
第4条：AIMessage AI思考消息
第5条：ToolMessage工具返回结果消息: 20度
(调用rag_summarize工具，返回扫地机器人在用户所在地区的气温下如何保养的总结)
第6条：AIMessage AI思考消息
第7条：ToolMessage工具返回结果消息: RAG检索出来的保养内容原文
"""



if __name__ == "__main__":
    agent = ReactAgent()

    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
