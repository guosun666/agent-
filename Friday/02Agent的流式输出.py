from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool(description="查询股票价格")
def get_price(name:str):
    return f"股票{name}的价格是100元"

@tool(description="获取股票信息，传入股票名称，返回字符串信息")
def get_info(name:str):
    return f"股票{name}的信息是：传智教育是一家专注于IT教育的公司，成立于2006年，总部位于北京。"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max",api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
    tools=[get_price,get_info],
    system_prompt="你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具"
)

res = agent.stream({
    "messages":[
        {"role":"user","content":"传智教育股价多少，并介绍一下"}
    ]
},
stream_mode = "values")    #stream_mode = "values" 是流式输出的模式，返回的是值，而不是消息

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
    