#this is my faiss python program. 

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Paths
DATA_PATH = "data"
FAISS_PATH = "faiss_gemini"

def ingest_documents():
    """Load, split, embed, and save documents to FAISS."""
    print("📥 Loading and processing documents...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-exp-03-07')
    db = FAISS.from_documents(chunks, embedding=embeddings)
    db.save_local(FAISS_PATH)

    print("✅ Embedding complete and saved to FAISS.")

def load_db_and_query(query_text: str) -> str:
    """Load FAISS DB and get answer for query."""
    print("🔍 Loading vector database...")
    embeddings = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-exp-03-07')
    db = FAISS.load_local(folder_path=FAISS_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant. Use only the following context to answer the question.
        Provide a clear and accurate answer.

        Context:
        {context}

        Question:
        {input}
        """
    )

    retriever = db.as_retriever(search_kwargs={"k": 5})
    doc_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, doc_chain)

    response = chain.invoke({"input": query_text})
    return response['answer'].strip()

if __name__ == "__main__":
    # Step 1: Ingest documents (only once needed; comment after first run if needed)
    ingest_documents()

    # Step 2: Ask questions
    while True:
        query_text = input("\n❓ Enter your query (or type 'exit' to quit): ")
        if query_text.lower() == "exit":
            break
        response = load_db_and_query(query_text)
        print("💬 Answer:", response)
