from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
import openai

####################################################
#                                                  #
# This file upserts documents in data to pinecone. #
#                                                  #
####################################################


load_dotenv()
openai.api_key = os.getenv('api_key')
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')
os.environ['PINECONE_API_KEY'] = os.getenv('pinecone_api_key')

index_name = "ruikang-guo-knowledge-base"

pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
pinecone_index = pc.Index(index_name)


if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(f"Environment variable OPENAI_API_KEY is not set")

# Load docs
def upsert_docs(input_dir: str, index_name: str):
    print(f"Building from {input_dir} under index {index_name}...\n")
    # documents = SimpleDirectoryReader(input_dir=input_dir).load_data()
    documents = SimpleDirectoryReader(input_dir).load_data()

    # create the index if it does not exist already
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print("Created brand new index...\n")
    else:
        pc.delete_index(index_name)
        print(f"Removed old index {index_name}...\n")
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print("Created replacement index...\n")

    # connect to the index
    pineconeIndex = pc.Index(index_name)

    vectorStore = PineconeVectorStore(
        pinecone_index=pineconeIndex
    )

    storage_context = StorageContext.from_defaults(vector_store=vectorStore)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    print(f"Done building !\n")

upsert_docs(input_dir="upsert_doc/docs", index_name="ruikang-guo-knowledge-base")
