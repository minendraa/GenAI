import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os
import shutil
import atexit # Import the atexit module

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Paths
CV_DATA_PATH = "cv_data"
FAISS_PATH = "faiss_openai_cv"

# Ensure folders exist at the start
os.makedirs(CV_DATA_PATH, exist_ok=True)
os.makedirs(FAISS_PATH, exist_ok=True)

# --- NEW CLEANUP FUNCTION FOR EXIT ---
def clean_on_exit():
    """Delete all files/subfolders inside cv_data and faiss_openai_cv but keep the folders."""
    print("\n🧹 Shutting down... Cleaning up temporary files.")
    
    def delete_folder_contents(folder_path):
        if os.path.exists(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    print(f"  - Deleted: {item_path}")
                except Exception as e:
                    print(f"❌ Error deleting {item_path}: {e}")

    delete_folder_contents(CV_DATA_PATH)
    delete_folder_contents(FAISS_PATH)
    print("✅ Cleanup complete.")

# --- REGISTER THE CLEANUP FUNCTION ---
# This function will now be called automatically when the script exits gracefully (e.g., Ctrl+C)
atexit.register(clean_on_exit)


# Streamlit page configuration
st.set_page_config(
    page_title="CV Analysis Assistant",
    page_icon="📄",
    layout="wide"
)

def check_faiss_index_exists():
    """Check if the essential FAISS index files exist."""
    index_file = os.path.join(FAISS_PATH, "index.faiss")
    pkl_file = os.path.join(FAISS_PATH, "index.pkl")
    return os.path.exists(index_file) and os.path.exists(pkl_file)

def clear_faiss_index():
    """Remove all contents of the FAISS directory."""
    if os.path.exists(FAISS_PATH):
        for item in os.listdir(FAISS_PATH):
            item_path = os.path.join(FAISS_PATH, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                st.error(f"Error deleting item {item_path}: {e}")

def save_uploaded_files(uploaded_files):
    """Save uploaded PDFs to the cv_data folder, clearing old ones first."""
    # This function is now just for saving, as cleanup is handled globally on exit
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith('.pdf'):
            file_path = os.path.join(CV_DATA_PATH, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
    return len(uploaded_files)


def ingest_cvs():
    """Load, split, embed, and save CVs to FAISS. This function now handles cleanup."""
    pdf_files = [f for f in os.listdir(CV_DATA_PATH) if f.lower().endswith('.pdf')]
    if not pdf_files:
        st.warning(f"No PDF files found in {CV_DATA_PATH}")
        clear_faiss_index() 
        return False

    with st.status("Processing CVs...", expanded=True) as status:
        try:
            status.write("Clearing old database...")
            clear_faiss_index()

            status.write("Loading PDF files...")
            docs = []
            for pdf_file in pdf_files:
                loader = PyPDFLoader(os.path.join(CV_DATA_PATH, pdf_file))
                docs.extend(loader.load())
            
            status.write(f"Loaded {len(docs)} pages from {len(pdf_files)} PDFs")
            
            status.write("Splitting documents into chunks...")
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            chunks = splitter.split_documents(docs)

            status.write("Creating embeddings and building FAISS index...")
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            
            db = FAISS.from_documents(chunks, embedding=embeddings)
            db.save_local(FAISS_PATH)
            
            status.update(label="Processing complete!", state="complete", expanded=False)
            st.success(f"Created FAISS index with {len(chunks)} chunks from {len(pdf_files)} CVs")
            return True
        except Exception as e:
            st.error(f"Error during ingestion: {str(e)}")
            status.update(label="Ingestion failed.", state="error", expanded=True)
            clear_faiss_index()
            return False

def query_cv(query_text: str) -> str:
    """Query the CV database."""
    with st.spinner("Searching CV database..."):
        try:
            if not check_faiss_index_exists():
                return "No CV database found. Please process CVs first."
                
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            db = FAISS.load_local(folder_path=FAISS_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
            
            llm = ChatOpenAI(model="gpt-4-turbo")

            prompt = ChatPromptTemplate.from_template(
                """You are an expert HR assistant analyzing CVs. Answer the question using only the provided context.
                Context: {context}
                Question: {input}
                Provide clear, concise answers. When listing names, include all candidates found. Format names as bullet points when listing multiple candidates."""
            )

            retriever = db.as_retriever(search_kwargs={"k": 5})
            chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
            
            response = chain.invoke({"input": query_text})
            return response['answer'].strip()
        except Exception as e:
            return f"Error processing query: {str(e)}"

def main():
    st.title("📄 CV Analysis Assistant")
    st.markdown("Upload and analyze candidate CVs using AI")
    
    if "cvs_ready" not in st.session_state:
        # On first run, it will correctly be false because clean_on_exit deleted the files
        st.session_state.cvs_ready = check_faiss_index_exists()
    
    if "query_history" not in st.session_state:
        st.session_state.query_history = []


    with st.sidebar:
        st.header("Upload CVs")
        uploaded_files = st.file_uploader(
            "Upload PDF CVs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload multiple PDF files containing candidate CVs"
        )
        
        if st.button("Process CVs", type="primary"):
            if uploaded_files:
                st.session_state.cvs_ready = False
                save_uploaded_files(uploaded_files)
                
                if ingest_cvs():
                    st.session_state.cvs_ready = True
                else:
                    st.session_state.cvs_ready = False
                
                st.rerun()
            else:
                st.warning("Please upload at least one PDF file first")
        
        st.markdown("---")
        st.subheader("CV Status")
        if st.session_state.cvs_ready:
            st.success("✅ CV database ready")
        else:
            st.warning("⚠️ No CV database found")

        st.markdown("---")
        st.subheader("Example Questions")
        examples = ["List all candidate names", "Who has Python experience?"]
        for example in examples:
            if st.button(example):
                st.session_state.query_text = example
                st.rerun()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Ask a Question")
        query_text = st.text_input(
            "Ask about candidates:",
            value=st.session_state.get("query_text", ""),
            placeholder="e.g. 'List all candidate names'",
            label_visibility="collapsed"
        )
        
        submit_disabled = not st.session_state.cvs_ready
        
        if st.button("Submit Query", disabled=submit_disabled):
            if query_text:
                answer = query_cv(query_text)
                st.session_state.query_history.append((query_text, answer))
                st.rerun()
            else:
                st.warning("Please enter a question.")

        if submit_disabled and not uploaded_files:
            st.info("Please upload and process CVs before submitting a query.")
            
        if st.session_state.query_history:
             st.subheader("Answer:")
             st.markdown(st.session_state.query_history[-1][1])
    
    with col2:
        st.subheader("Query History")
        if st.session_state.query_history:
            for q, a in reversed(st.session_state.query_history[:-1]):
                with st.expander(f"Q: {q[:30]}..."):
                    st.markdown(f"**Answer:**\n\n{a}")
        else:
            st.info("Your query history will appear here")

if __name__ == "__main__":
    main()