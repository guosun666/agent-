from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi

#示例的模板
example_template = PromptTemplate.from_template(
    "单词：{word}，反义词：{antonym}"
)
#示例的动态数据注入，要求是list当中内套字典
examples_data = [
    {"word":"happy","antonym":"sad"},
    {"word":"tall","antonym":"short"},
    {"word":"big","antonym":"small"},
    {"word":"fast","antonym":"slow"},
    {"word":"good","antonym":"bad"},
]


few_shot_prompt_template = FewShotPromptTemplate(
    example_prompt=example_template,   #示例模板
    examples=examples_data,            #示例数据用来注入动态数据,list当中内套字典
    prefix="告诉我单词的反义词，我提供如下的示例:",       #示例之前的提示词
    suffix="基于前面的案例，{input}的反义词是：",        #示例之后的提示词
    input_variables=["input"]     #声明在前缀或后缀中所需要注入的变量名
)

res = few_shot_prompt_template.invoke({"input":"left"}).to_string()
model = Tongyi(model="qwen-turbo", api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

print(model.invoke(res))


