"""
基于Python前端快捷式框架Streamlit完成WEB页面上传服务
"""
import streamlit as st

st.title("知识库更新服务")

uploader_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False,    #False表示仅接受一个文件的上传   
)

if uploader_file is not None:
    #提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size/1024    #文件大小，单位为KB

    st.subheader(f"文件信息：{file_name}")   #加了f是指将变量自动插入到字符串中
    st.write(f"格式：{file_type} | 大小：{file_size:.2f}KB")
    #显示文件内容  getvalue  -->获得字节流bytes --> decode("utf-8") --> 解码为字符串
    text = uploader_file.getvalue().decode("utf-8")
    st.write(text)