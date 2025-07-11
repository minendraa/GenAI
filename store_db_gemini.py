from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

DATA_PATH="data"
FAISS_PATH="faiss_gemini"

document_loader = PyPDFDirectoryLoader(DATA_PATH)
docs=document_loader.load()

text_splitter =RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents=text_splitter.split_documents(docs)

db=FAISS.from_documents(embedding=GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-exp-03-07'), documents=documents)
db.save_local(FAISS_PATH)