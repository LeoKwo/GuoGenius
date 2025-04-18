from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
# from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
import os
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from dotenv import load_dotenv
import openai
from langchain.tools import DuckDuckGoSearchRun, Tool
from langchain.utilities import WikipediaAPIWrapper
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

# Connect to Pinecone
index_name = "ruikang-guo-knowledge-base"
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
pinecone_index = pc.Index(index_name)

# Ruikang Guo QA Tool
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context
)

rkguo_query_engine = index.as_query_engine()
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
