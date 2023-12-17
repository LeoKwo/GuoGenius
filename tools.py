from typing import Optional
import pinecone
from llama_index.vector_stores import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from llama_index.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index import ServiceContext, GPTVectorStoreIndex
from dotenv import load_dotenv
import openai
from langchain.tools import DuckDuckGoSearchRun, Tool, HumanInputRun
from langchain.utilities import SerpAPIWrapper, WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI
import requests
import json
from duckduckgo_search import DDGS
# from langchain. vectorstores import Pinecone

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('api_key')
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')
os.environ['PINECONE_API_KEY'] = os.getenv('pinecone_api_key')
os.environ['PINECONE_ENVIRONMENT'] = os.getenv('pinecone_env')
sampro_api_key = os.getenv('sampro_api_key')

# Connect to Pinecone
index_name = "ruikang-guo-knowledge-base"
pinecone.init(
    api_key=os.environ['PINECONE_API_KEY'],
    environment=os.environ['PINECONE_ENVIRONMENT']
)
pinecone_index = pinecone.Index(index_name)
embed_model = OpenAIEmbedding(model='text-embedding-ada-002', embed_batch_size=100)
service_context = ServiceContext.from_defaults(embed_model=embed_model)

# Ruikang Guo QA Tool
rkguo_vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
)
rkguo_index = GPTVectorStoreIndex.from_vector_store(
    vector_store=rkguo_vector_store,
    service_context=service_context
)
rkguo_query_engine = rkguo_index.as_query_engine()
rkguo_tool = QueryEngineTool(
    query_engine=rkguo_query_engine,
    metadata=ToolMetadata(
        name="ruikang_guo_factual_qa_tool",
        description="Information about Ruikang Guo. Contains information from his resume, a list of his tech stacks, and his cover letter."
    )
)
rkguo_lc_tool = rkguo_tool.to_langchain_tool()

# DuckDuckGoSearch
ddg_search = DuckDuckGoSearchRun()
ddg_search_lc_tool = Tool(
    name="DuckDuckGoSearch",
    func=ddg_search.run,
    description="Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
)

# Wikipedia
wikipedia = WikipediaAPIWrapper()
wikipedia_lc_tool = Tool(
    name="WikipediaSearch",
    func=wikipedia.run,
    description="Useful for when you need to look up a topic, event or person on wikipedia"
)

# Calculator
math = LLMMathChain.from_llm(OpenAI())
math_lc_tool = Tool(
    name="Calculator",
    func=math.run,
    description="Useful for when you need to do math calculations."
)
