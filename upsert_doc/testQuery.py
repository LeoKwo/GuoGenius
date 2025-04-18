import os
from dotenv import load_dotenv
import openai
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex

##################################################
#                                                #
# This file tests pinecone connection and query. #
#                                                #
##################################################

load_dotenv()
openai.api_key = os.getenv('api_key')
os.environ['PINECONE_API_KEY'] = os.getenv('pinecone_api_key')

index_name = "ruikang-guo-knowledge-base"

pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
pinecone_index = pc.Index(index_name)

vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context
)

query_engine = index.as_query_engine()
res = query_engine.query("What can you tell me about ruikang guo's work at day and nite?")
print(res)