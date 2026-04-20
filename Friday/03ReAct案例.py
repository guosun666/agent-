from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool(description="获取体重，返回值是整数，单位是千克")
def get_weight() -> int:
    return 90

@tool(description="获取身高，返回值是整数，单位是厘米")
def get_height() -> int:
    return 180

agent = create_agent(
    model=ChatTongyi(model="qwen3-max",api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
    tools=[get_weight, get_height],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
    且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
    并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""",
)


res = agent.stream({
    "messages":[
        {"role":"user","content":"我的体重是多少，身高是多少，计算我的BMI指数"}
    ]
},
stream_mode = "values")

for chunk in res:
    latest_message = chunk["messages"][-1]

    if latest_message.content:
        print(f"{type(latest_message).__name__}:{latest_message.content}")
    #这里latest_message.tool_calls是简写，等价于latest_message.additional_kwargs["tool_calls"]
    
    #因为有的消息没有tool_calls，所以需要捕获AttributeError异常
    try:
        if latest_message.tool_calls:
            print(f"工具调用：{[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError as e:
        pass
    