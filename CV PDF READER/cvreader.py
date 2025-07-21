from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Paths
CV_DATA_PATH = "cv_data"  # Folder containing CV PDFs
FAISS_PATH = "faiss_openai_cv"

def ingest_cvs():
    """Load, split, embed, and save CVs to FAISS."""
    print("📥 Loading and processing CVs...")
    loader = PyPDFDirectoryLoader(CV_DATA_PATH)
    docs = loader.load()

    # Split text with smaller chunks for CVs (better for extracting specific details)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.from_documents(chunks, embedding=embeddings)
    db.save_local(FAISS_PATH)

    print(f"✅ Embedding complete. Processed {len(chunks)} chunks from CVs.")

def query_cv(query_text: str) -> str:
    """Load FAISS DB and get answer about CVs."""
    print("🔍 Loading CV database...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.load_local(folder_path=FAISS_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)

    # Using GPT-4 for better understanding of CV content
    llm = ChatOpenAI(model="gpt-4-turbo")

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert HR assistant analyzing CVs. Use only the provided CV information to answer.
        Be precise and extract relevant details from the CVs.

        Context from CVs:
        {context}

        Question:
        {input}

        Provide the most relevant information found in the CVs. If asking about specific candidates,
        mention their name and the relevant details from their CV.
        """
    )

    retriever = db.as_retriever(search_kwargs={"k": 3})  # Fewer but more relevant chunks for CVs
    doc_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, doc_chain)

    response = chain.invoke({"input": query_text})
    return response['answer'].strip()

if __name__ == "__main__":
    # Step 1: Ingest CVs (run once initially)
    # ingest_cvs()  # Uncomment to process CVs, then comment after first run

    # Step 2: Query CV database
    print("\nCV Analysis Assistant (type 'exit' to quit)")
    print("Example questions:")
    print("- Who has learned Python and machine learning?")
    print("- Give name of all the candidates.")
    #print("- List all candidates with MBA degrees")
    
    while True:
        query_text = input("\n❓ What would you like to know about the candidates? ")
        if query_text.lower() in ['exit', 'quit']:
            break
        response = query_cv(query_text)
        print("\n💬 CV Analysis Result:")
        print(response)