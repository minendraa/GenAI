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
CV_DATA_PATH = "cv_data"
FAISS_PATH = "faiss_openai_cv"

def ingest_cvs():
    """Load, split, embed, and save CVs to FAISS if index doesn't exist."""
    # First check if there are any PDF files
    pdf_files = [f for f in os.listdir(CV_DATA_PATH) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"⚠️ No PDF files found in {CV_DATA_PATH}")
        return

    # Check if FAISS index exists
    if (os.path.exists(os.path.join(FAISS_PATH, "index.faiss")) and 
        os.path.exists(os.path.join(FAISS_PATH, "index.pkl"))):
        print(f"⏩ FAISS index already exists with {len(pdf_files)} PDFs. Skipping ingestion.")
        return

    print(f"📥 Processing {len(pdf_files)} CVs...")
    try:
        loader = PyPDFDirectoryLoader(CV_DATA_PATH)
        docs = loader.load()
        
        if len(docs) != len(pdf_files):
            print(f"⚠️ Warning: Loaded {len(docs)} documents but found {len(pdf_files)} PDF files")
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        db = FAISS.from_documents(chunks, embedding=embeddings)
        
        os.makedirs(FAISS_PATH, exist_ok=True)
        db.save_local(FAISS_PATH)
        
        print(f"✅ Created FAISS index with {len(chunks)} chunks from {len(docs)} CVs")
    except Exception as e:
        print(f"❌ Error during ingestion: {str(e)}")

def query_cv(query_text: str) -> str:
    """Query the CV database."""
    print("🔍 Loading CV database...")
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        db = FAISS.load_local(folder_path=FAISS_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
        
        llm = ChatOpenAI(model="gpt-4-turbo")

        # Simplified prompt without template logic
        prompt = ChatPromptTemplate.from_template(
            """You are an expert HR assistant analyzing CVs. Answer the question using only the provided context.
            
            Context: {context}
            
            Question: {input}
            
            Provide clear, concise answers. When listing names, include all candidates found."""
        )

        retriever = db.as_retriever(search_kwargs={"k": 5})
        chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
        
        response = chain.invoke({"input": query_text})
        return response['answer'].strip()
    except Exception as e:
        return f"Error processing query: {str(e)}"

if __name__ == "__main__":
    # First run ingestion (comment out after first run)
    ingest_cvs()

    # Query interface
    print("\nCV Analysis Assistant (type 'exit' to quit)")
    print("Example questions:")
    print("- List all candidate names")
    print("- Who has Python experience?")
    
    while True:
        try:
            query_text = input("\n❓ What would you like to know about the candidates? ")
            if query_text.lower() in ['exit', 'quit']:
                break
            response = query_cv(query_text)
            print("\n💬 Answer:")
            print(response)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")