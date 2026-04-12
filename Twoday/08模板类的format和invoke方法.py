from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate



template = PromptTemplate.from_template("我的邻居姓{last_name}，名{first_name}，他的年龄是{age}岁")

res = template.format(last_name="张",first_name="三",age=18)
print(res,type(res))

res = template.invoke({"last_name":"张","first_name":"三","age":18})
print(res.to_string(),type(res))





