from dotenv import load_dotenv
import os
from pinecone import Pinecone
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings 
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE

extracted_data = load_pdf_files(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)


embeddings = download_embeddings()

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)


index_name = "medical-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric = "cosine",
        spec = ServerlessSpec(cloud="aws", region = "us-east-1")
    )


index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name
)