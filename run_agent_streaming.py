import streamlit as st
import re
from agent_streaming import agent

def run_agent(prompt) -> str:
    result_holder = {}
    full_output_holder = {"text": ""}

    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.spinner(text="🧠"):
            async def wrapper_gen():

                async for chunk in agent(
                    prompt=prompt,
                    result_holder=result_holder
                ):
                    print(chunk, end="", flush=True)
                    yield chunk
            
            st.write_stream(wrapper_gen)

    streaming_placeholder.empty()

    full_output = full_output_holder["text"]

    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    st.markdown(main_output)

    return result_holder.get("result")