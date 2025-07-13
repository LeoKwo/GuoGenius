import streamlit as st
from PIL import Image
from pathlib import Path
from run_agent_streaming import run_agent

st.set_page_config(page_title="GuoGenius", page_icon="💡")
st.title("💡 GuoGenius")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant", 
            "content": "你好👋 我是GuoGenius。我是郭睿康的数字化分身，拥有关于他的职业经历和技能的一切信息。我可以回答您的任何问题，让我们开始吧！"
        },
    ]

with st.expander("💡 了解更多", expanded=False):
    st.success("""
        💡 GuoGenius是郭睿康的数字化分身，拥有关于他的职业经历和技能的一切信息。
    """)
    st.info("""
        #### GuoGenius 技术栈
        ```
        Streamlit
        LangChain
        DeepSeek-V3
        阿里云轻量化服务器
        ```
        此项目已开源：[https://github.com/LeoKwo/GuoGenius](https://github.com/LeoKwo/GuoGenius)\n
        *中文版与英文版略有不同。
    """)

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant", avatar=Image.open(Path("./pics/bot.jpg"))).write(msg["content"])

    else:
        st.chat_message("user", avatar="😎").write(msg["content"])

if question := st.chat_input("您的问题 ..."):            
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message(name="user", avatar="😎").write(question)
    with st.chat_message(name="assistant", avatar=Image.open(Path("./pics/bot.jpg"))):
        response = run_agent(prompt=question)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)