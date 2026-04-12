from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

#zero-shot提示词模板
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name}，名{first_name}，他的年龄是{age}岁"
)
# #调用format方法，注入信息
# prompt_text = prompt_template.format(last_name="张",first_name="三",age=18)

# model = Tongyi(model="qwen-turbo", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")
# res = model.invoke(prompt_text)
# print(res)

#为什么要用这种方法是因为：使用Template模板时方便大型工程做标准化模板。支持LangChain的链式调用

model = Tongyi(model="qwen-turbo", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

chain = prompt_template | model
res = chain.invoke(input={"last_name":"张","first_name":"三","age":18})
print(res)
