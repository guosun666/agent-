from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/pdf2.pdf",
    mode="single",              #默认是page模式，每个页面生成一个Document文档对象
                                #single模式：不管有多少页面，只返回一个Document对象
    password="itheima"          #pdf文件的密码
    )


i=0
for document in loader.lazy_load():
    i+=1
    print(document,i)
    print("-"*100,i)





