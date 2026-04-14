from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings


prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个专家，简洁回答问题,参考文献是：{context}"),
    ("user","用户提问是{input},不用回复参考文献"),
])

model = ChatTongyi(model="qwen3-max",api_key="sk-e90151cacd374f6b865b54c2fe14f1fd")

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(dashscope_api_key="sk-e90151cacd374f6b865b54c2fe14f1fd"),
)
# add_texts（List[str]） 添加文本到向量存储当中
vector_store.add_texts(["减肥就是要少吃多练","减脂期间吃很重要","跑步很重要"])

input_text = "怎么减肥?"

#向量检索
results = vector_store.similarity_search(input_text,k=3)
#构建参考文献
reference_text ="["+",".join([result.page_content for result in results])+"]"

def get_prompt(prompt):
    print("-"*100)
    print(prompt.to_string())
    print("-"*100)
    return prompt
#构建chain
chain = prompt | get_prompt | model | StrOutputParser()

#执行chain
response = chain.invoke({"context":reference_text,"input":input_text})
print(response)