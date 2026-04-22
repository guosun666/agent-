from rag import RagService
import streamlit as st
import config_data as config


st.title("智能客服")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "你好，有什么可以帮助你？"}
    ]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("你的信息")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    agent_response = []
    error_text = ""

    with st.spinner("AI思考中..."):
        try:
            for chunk in st.session_state["rag"].chain.stream(
                {"input": prompt}, config.session_config
            ):
                agent_response.append(chunk)
        except Exception as exc:
            error_text = f"AI服务异常，请稍后重试：{exc}"

    assistant_response = "".join(agent_response).strip()
    if error_text:
        st.chat_message("assistant").write(error_text)
    elif assistant_response:
        st.chat_message("assistant").write(assistant_response)
        st.session_state["message"].append(
            {"role": "assistant", "content": assistant_response}
        )
