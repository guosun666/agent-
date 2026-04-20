"""
基于Python前端快捷式框架Streamlit完成WEB页面上传服务

Streamlit：当Web页面元素发生变化，则代码重新执行一遍
"""
import time
import streamlit as st
from knowledge_base import KnowledgeBaseService



st.title("知识库更新服务")

uploader_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False,    #False表示仅接受一个文件的上传   
)
# Streamlit框架，提供了session_state，可以存储一些数据，避免重复创建对象，浪费资源
#session_state就是一个字典，key是service，value是KnowledgeBaseService对象，
#程序不停创建一个类对象比较好，避免重复创建对象，浪费资源
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    #提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size/1024    #文件大小，单位为KB

    st.subheader(f"文件信息：{file_name}")   #加了f是指将变量自动插入到字符串中
    st.write(f"格式：{file_type} | 大小：{file_size:.2f}KB")

    #显示文件内容  getvalue  -->获得字节流bytes --> decode("utf-8") --> 解码为字符串
    text = uploader_file.getvalue().decode("utf-8")
    #with语法：自动进入，自动退出
    with st.spinner("正在更新知识库..."):         #spinner是显示一个加载动画，会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)
