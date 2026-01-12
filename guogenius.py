import streamlit as st
from PIL import Image
from pathlib import Path
from run_agent_streaming import run_agent
from translation import translate

st.set_page_config(page_title="GuoGenius", page_icon="💡")
st.title("💡 GuoGenius")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant", 
            "content": "Hi I am GuoGenius. I am Ruikang Guo's digital persona. How can I help you today? 你好👋 我是GuoGenius，郭睿康的数字化分身，让我们开始吧！"
        },
    ]

language = st.selectbox(label="Language / 语言", options=[
    "English",
    "中文"
])

languageIsEnglish = language == "English"

with st.expander(translate("more", languageIsEnglish), expanded=False):
    st.success(translate("info", languageIsEnglish))
    st.info(translate("techstack", languageIsEnglish))

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant", avatar=Image.open(Path("./pics/bot.jpg"))).write(msg["content"])

    else:
        st.chat_message("user", avatar="😎").write(msg["content"])

if question := st.chat_input(translate("yourquestion", languageIsEnglish)):            
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message(name="user", avatar="😎").write(question)
    with st.chat_message(name="assistant", avatar=Image.open(Path("./pics/bot.jpg"))):
        response = run_agent(prompt=question)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)