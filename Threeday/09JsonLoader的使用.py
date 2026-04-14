from langchain_community.document_loaders import JSONLoader

#单个JSON对象
# loader = JSONLoader(
#     file_path="./data/stu.json",
#     jq_schema=".",
#     text_content=False, #告知JSONLoader,我抽取的内容不是字符串，是JSON对象
# )

# documents = loader.load()
# print(documents)

#数组中多个JSON对象
# loader = JSONLoader(
#     file_path="./data/stus.json",
#     jq_schema=".[].name",
#     text_content=False, #告知JSONLoader,我抽取的内容不是字符串，是JSON对象
# )

# document = loader.load()
# print(document)

#JSON行
loader = JSONLoader(
    file_path="./data/stu_json_lines.json",  #必填
    jq_schema=".name", #必填
    text_content=False, #告知JSONLoader,我抽取的内容不是字符串，是JSON对象    选填
    json_lines=True, #告知JSONLoader,我抽取的内容是JSON对象，是JSON行        选填
)

documents = loader.load()
print(documents)