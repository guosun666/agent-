import streamlit as st

from agent.react_agent import ReactAgent
from utils.logger_handler import logger


st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("你的信息")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_chunks = []

    def stream_response():
        try:
            for chunk in st.session_state["agent"].execute_stream(prompt):
                response_chunks.append(chunk)
                yield chunk
        except Exception as exc:
            logger.exception("[streamlit] assistant response failed")
            yield f"\n\n抱歉，智能客服运行时出错：{exc}"
            response_chunks.append(error_text)
            yield error_text

    with st.spinner("智能客服思考中..."):
        st.chat_message("assistant").write_stream(stream_response())

    assistant_response = "".join(response_chunks).strip()
    if assistant_response:
        st.session_state["message"].append(
            {"role": "assistant", "content": assistant_response}
        )

