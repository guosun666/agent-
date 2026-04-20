from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser



@tool(description="查询天气")
def get_weather():
    return "明天深圳的天气晴朗，气温20-25度"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max",api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题"
)

parser = StrOutputParser()

result = agent.invoke({"messages":[{"role":"user","content":"明天深圳的天气怎么样?"}]})
for msg in result["messages"]:
    print(f"{type(msg).__name__}:{parser.invoke(msg)}")

    #parser.invoke(msg) 将msg转换为字符串等价于msg.content
