from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationTokenBufferMemory
from langchain.schema.messages import SystemMessage
import streamlit as st
from langchain.chat_models import ChatOpenAI
import os
import openai
from dotenv import load_dotenv
from tools import rkguo_lc_tool, ddg_search_lc_tool, math_lc_tool
from PIL import Image
from pathlib import Path

load_dotenv()
openai.api_key = os.getenv('api_key')
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')

st.set_page_config(page_title="GuoGenius", page_icon="💡")
st.title("💡 GuoGenius")

# Define session state messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant", 
            "content": "Hi I am GuoGenius. I am Ruikang Guo's digital persona. How can I help you today?"
        },
    ]

with st.expander("💡 Learn more about GuoGenius", expanded=False):
    st.info("""
        💡 GuoGenius is the digital persona of Ruikang Guo. Ask him any question about Ruikang Guo.
    """)
    st.info("""
        1. Ruikang Guo's Resume
        2. Ruikang Guo's General Information
        3. Math calculations,
        4. Search web for additional information.
    """)

# Define LLM
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", streaming=True)

# Define tools
tools = [
    rkguo_lc_tool,
    ddg_search_lc_tool,
    math_lc_tool,
]

# Define starter identity prompt
prompt = OpenAIFunctionsAgent.create_prompt(
    SystemMessage(content=(
        "You are GuoGenius created by Ruikang Guo or Leo Guo. You are Ruikang Guo's digital persona tasked answering questions about the Ruikang Guo's professional experiences, education backgrounds, and other career related topics. "
        "You have access to a Ruikang Guo knowledge bank which you can query but know NOTHING about Ruikang Guo otherwise. "
        "You should always first query the knowledge bank for information on the concepts in the question. "
        "For example, given the following input question:\n"
        "-----START OF EXAMPLE INPUT QUESTION-----\n"
        "How did Ruikang Guo perform in his current job at Day & Nite? \n"
        "-----END OF EXAMPLE INPUT QUESTION-----\n"
        "Your research flow should be:\n"
        "1. Query your rkguo_lc_tool for information on 'work' to get as much context as you can about it.\n"
        "2. Answer the question with the context you have gathered."
        "If you can't find the answer, DO NOT make up an answer. Just say you don't know. "
        "Answer the following question as best you can:")
    ),
)

memory = ConversationTokenBufferMemory(memory_key="chat_history", llm=llm, max_token_limit=2000, human_prefix="user", ai_prefix="assistant")

if st.session_state.messages: 
    for message in st.session_state.messages:
        if message["role"] == "user":
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

agent_chain = AgentExecutor(
    agent=agent, tools=tools, verbose=True, memory=memory
)

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant", avatar=Image.open(Path("./pics/bot.jpg"))).write(msg["content"])

    else:
        st.chat_message("user", avatar="😎").write(msg["content"])

if prompt := st.chat_input(placeholder="Your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="😎").write(prompt)
    with st.chat_message("assistant", avatar=Image.open(Path("./pics/bot.jpg"))):
        st.write("🧠 Thinking...")
        st_callback_handler = StreamlitCallbackHandler(st.container())
        try:
            response = agent_chain.run(prompt, callbacks=[st_callback_handler])

        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                # raise error
                response = f"{response.replace('Could not parse LLM output:', '')}"
                response.replace("Could not parse LLM output:", "")
            else:
                response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
        