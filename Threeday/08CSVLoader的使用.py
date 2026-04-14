from langchain_community.document_loaders import CSVLoader



loader = CSVLoader(
    file_path="./data/stu.csv",
    csv_args={
        "delimiter":",",
        "quotechar":'"',
        #如果数据没有表头，这里可以指定表头，如果有则不要用
        "fieldnames":["a","b","c","d"],
    },
    encoding="utf-8",  # Windows 默认 gbk；本 CSV 为 UTF-8 中文
)


#批量加载 .load() 返回的是列表，每个元素是一个Document类对象
# data = loader.load()

# for d in data:
#     print(d,type(d))

# 惰性加载 .lazy_load() 返回的是生成器，每次返回一个Document类对象
for document in loader.lazy_load():
    print(document)