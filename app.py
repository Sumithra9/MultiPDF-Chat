import os
import streamlit as st
import tempfile
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Streamlit setup
st.set_page_config(page_title="📚 Multi-PDF Chatbot", layout="wide")
st.title("📚 Multi-PDF Chatbot using Groq + LangChain")

# Upload PDFs
uploaded_files = st.file_uploader("Upload multiple PDF files", type=["pdf"], accept_multiple_files=True)

# Input query
query = st.text_input("Ask a question based on the uploaded PDFs")

# Load Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.warning("Please set your GROQ_API_KEY in a .env file.")
    st.stop()

# Main logic
if uploaded_files and query:
    with st.spinner("🔍 Processing..."):
        try:
            # Load PDF content
            docs = []
            for uploaded_file in uploaded_files:
                st.write(f"📄 Reading {uploaded_file.name}...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    loader = PyPDFLoader(tmp_file.name)
                    docs.extend(loader.load())

            # Split text into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(docs)

            # Generate embeddings
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            # Create FAISS vector store
            vectorstore = FAISS.from_documents(chunks, embeddings)
            retriever = vectorstore.as_retriever(search_type="similarity", k=3)

            # Use Groq's LLaMA 3 model
            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama3-8b-8192"
            )

            # Create RetrievalQA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                return_source_documents=True
            )

            # Run the query properly (not .run())
            result = qa_chain({"query": query})

            # Display answer
            st.subheader("🧠 Answer")
            st.success(result["result"])

            # Display source documents
            st.subheader("📄 Source Documents")
            for i, doc in enumerate(result["source_documents"]):
                st.markdown(f"**Source {i+1}:**")
                st.code(doc.page_content[:500] + "...")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
