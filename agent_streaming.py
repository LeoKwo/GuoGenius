from langchain_core.prompts import PromptTemplate
from langchain_deepseek.chat_models import ChatDeepSeek
import os
from dotenv import load_dotenv
from doc_loader import pdf_to_str, txt_to_str
load_dotenv()

async def agent(
        prompt,
        result_holder,
        resume: str = pdf_to_str("./docs/Ruikang Guo Resume.pdf"),
        coverLetter: str  = pdf_to_str("./docs/Ruikang Guo Cover Letter.pdf"),
        techStack: str = txt_to_str("./docs/Tech Stacks.txt")
    ):

    model = ChatDeepSeek(
        model="deepseek-chat",
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        temperature=0.8
    )

    prompt_template = PromptTemplate.from_template("""
    郭睿康（Leo Guo）创造的 GuoGenius。
    你是郭睿康的数字化人格，负责回答关于郭睿康的专业经验、教育背景以及其他与职业相关的话题的问题。
    你可以查询郭睿康知识库以获取信息，但除此之外对郭睿康一无所知。

    根据郭睿康的简历和其他个人信息回答。如果以下提供的文件没办法回答用户的问题，直接表明此问题无法
    回答，千万不要随便编一个答案。

    【郭睿的简历】
    {resume}

    【郭睿康的技术栈】
    {techStack}

    【郭睿康的求职信】
    {coverLetter}

    【请注意】   
    用户可能用以下的名字称呼郭睿康：
    - 郭睿康
    - 睿康
    - Leo Guo
    - Leo
    - Ruikang Guo
    - Ruikang
    - 这个人
    等等
                                        
    --------------------------
    跟用户友好的交流，以下是他们的问题：
    {question}
    """)

    chain = prompt_template | model

    output_chunks = []

    async for event in chain.astream_events({
        "resume": resume,
        "coverLetter": coverLetter,
        "techStack": techStack,
        "question": prompt
    }):
        kind = event['event']
        if kind == "on_chat_model_stream":
            content = event['data']["chunk"].content
            output_chunks.append(content)
            yield content

    result = "".join(output_chunks)

    result_holder["result"] = result