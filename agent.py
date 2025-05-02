from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationTokenBufferMemory
from langchain.schema.messages import SystemMessage
import streamlit as st
from langchain_community.chat_models.tongyi import ChatTongyi
import os
from dotenv import load_dotenv
from tools import resumeTool
from PIL import Image
from pathlib import Path
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

load_dotenv()

# define Tongyi LLM
model = ChatTongyi(
      model='qwen-turbo',
      api_key=os.getenv('DASHSCOPE_API_KEY'),
)

st.set_page_config(page_title="GuoGenius", page_icon="💡")
st.title("💡 GuoGenius")

# Define session state messages
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
        LlamaIndex
        通义千问Turbo (qwen-turbo)
        阿里云通用文本向量模型-v3 (text-embedding-v3)
        阿里云轻量化服务器
        ```
        此项目已开源：[https://github.com/LeoKwo/GuoGenius](https://github.com/LeoKwo/GuoGenius)
    """)

# Define Tools for the bot
tools = [resumeTool]
tool_node = ToolNode(tools)

# define memory
memory = MemorySaver()

# define LLM agent executor
agent_executor = create_react_agent(
    model=model, tools=tools, checkpointer=memory
)

# Define starter identity prompt
prompt = OpenAIFunctionsAgent.create_prompt(
    SystemMessage(content=("""
            郭睿康（Leo Guo）创造的 GuoGenius。
            你是郭睿康的数字化人格，负责回答关于郭睿康的专业经验、教育背景以及其他与职业相关的话题的问题。
            你可以查询郭睿康知识库以获取信息，但除此之外对郭睿康一无所知。
            在回答问题时，你应该始终首先查询知识库中与问题概念相关的信息。

            例如，给定以下输入问题：
            —–示例输入问题开始—–
            郭睿康在 Day & Nite 的现任工作中表现如何？
            —–示例输入问题结束—–
            你的研究流程应为：
                1.	查询你的知识库工具（resumeTool），获取关于“工作”的相关上下文信息。
                2.	根据你收集的上下文回答问题。
            如果找不到答案，绝不要编造答案。直接说明你不知道即可。
            
            尽可能完整地回答以下问题：
        """)
    ),
)

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant", avatar=Image.open(Path("./pics/bot.jpg"))).write(msg["content"])

    else:
        st.chat_message("user", avatar="😎").write(msg["content"])

if prompt := st.chat_input(placeholder="您的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="😎").write(prompt)
    with st.chat_message("assistant", avatar=Image.open(Path("./pics/bot.jpg"))):
        st.write("🧠 Thinking...")
        st_callback_handler = StreamlitCallbackHandler(st.container())
        try:
            # print(prompt)
            response = agent_executor.invoke({
                        "messages": [
                            ("user", prompt)
                        ]
                    },
                    {"configurable": {"thread_id": 0}}
                )["messages"][-1].content
            # response = agent_chain.run(prompt, callbacks=[st_callback_handler])

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
        