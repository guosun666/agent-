from langchain_community.embeddings import DashScopeEmbeddings

model = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key="sk-e90151cacd374f6b865b54c2fe14f1fd",
)

print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","我爱你","我想你"]))

