from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document


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

def format_func(docs):
    if not docs:
        return "无相关参考资料"
    formatted_str = "[" + ", ".join([doc.page_content for doc in docs]) + "]"
    return formatted_str

def print_func(output):
    print("-"*100)
    print(output.to_string())
    print("-"*100)
    return output

#RunnablePassthrough 用于传递上下文,能不能把用户提问和检索信息也入链？
# # retriever:
#         -输入：用户的提问       str
#         -输出：向量库的检索结果   List[Document]
# # prompt:
#         -输入：用户的提问+向量库的检索结果     dict/list[dict]
#         -输出：完整的提示词       PromptValue

# langchain中向量存储对象，有一种方法：as_retriever()，可以返回一个Runnable接口的子类实例对象可以入链
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

chain = ({"context":retriever | format_func,"input":RunnablePassthrough()}| prompt | print_func | model | StrOutputParser())
response = chain.invoke(input_text)
print(response)