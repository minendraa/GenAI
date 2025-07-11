import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FAISS_PATH = "faiss_gemini"

# Load DB and RAG chain once
@st.cache_resource
def setup_rag_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-exp-03-07')
    db = FAISS.load_local(
        folder_path=FAISS_PATH,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_kwargs={"k": 5})

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant. Use the context below to answer the question in detail.

        Context:
        {context}

        Question:
        {input}
        """
    )
    doc_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, doc_chain)
    return chain

# Streamlit UI
st.set_page_config(page_title="Rag Chatbot", page_icon="🤖", layout="centered")
st.title("🛕 Chatbot for Temples in Nepal")
st.write("Ask questions from your embedded PDF documents.")

# Input
query_text = st.text_input("Enter your query:", placeholder="Ask something about your data...")

if query_text:
    with st.spinner("Thinking... 🤔"):
        chain = setup_rag_chain()
        response = chain.invoke({"input": query_text})
        st.markdown("### 💬 Answer:")
        st.success(response["answer"].strip())
