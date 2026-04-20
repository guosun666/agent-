from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent,AgentState
from langgraph.runtime import Runtime
from langchain.tools import tool
from langchain.agents.middleware import before_agent, after_agent,before_model, after_model,wrap_model_call,wrap_tool_call

@tool(description="获取天气，传入城市名称，返回城市天气")
def get_weather(city:str):
    return f"城市{city}的天气是晴天"


"""
1：agent执行前
2：agent执行后
3：model执行前
4：model执行后
5：工具执行中
6：模型执行中

"""
# agent在执行前会调用这个函数，并传入state和runtime两个对象
@before_agent
def log_before_agent(state:AgentState,runtime:Runtime):
    print(f"agent执行前，附带了{len(state['messages'])}个消息")

@after_agent
def log_after_agent(state:AgentState,runtime:Runtime):
    print(f"agent执行后，附带了{len(state['messages'])}个消息")



@before_model
def log_before_model(state:AgentState,runtime:Runtime):
    print(f"model执行前，附带了{len(state['messages'])}个消息")

@after_model
def log_after_model(state:AgentState,runtime:Runtime):
    print(f"model执行后，附带了{len(state['messages'])}个消息")

@wrap_model_call
def model_call_hook(request,handler):
    print("模型调用了")
    return handler(request)

@wrap_tool_call
def monitor_tool(request,handler):
    print(f"工具执行:{request.tool_call['name']}")
    print(f"工具执行传入的参数:{request.tool_call['args']}")
    return handler(request)




agent = create_agent(
    model=ChatTongyi(model="qwen3-max",api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
    tools=[get_weather],
    system_prompt="你是一个智能助手，可以回答用户问题，并且可以调用工具获取天气信息 ",
    middleware=[log_before_agent,log_after_agent,log_before_model,log_after_model,monitor_tool,model_call_hook]
)

res=agent.invoke({
    "messages":[
        {"role":"user","content":"深圳的天气怎么样？如何穿衣"}
    ]
})

print("========================\n",res)