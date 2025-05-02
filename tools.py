from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import os
from llama_index.core import Settings
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
from langchain_core.tools import tool

load_dotenv()

Settings.embed_model = DashScopeEmbedding(
    model_name='text-embedding-v3',
    text_type='document',
    api_key=os.getenv('DASHSCOPE_API_KEY')
)
documents = SimpleDirectoryReader("./docs").load_data()

index = VectorStoreIndex.from_documents(documents)

# Initialize DashScope object
dashscope_llm = DashScope(model_name=DashScopeGenerationModels.QWEN_TURBO, api_key=os.getenv('DASHSCOPE_API_KEY'))

chat_engine = index.as_chat_engine(llm=dashscope_llm)

@tool
def resumeTool(q: str):
    """Call to get information about Ruikang Guo."""
    return chat_engine.chat(q)

