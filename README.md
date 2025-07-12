# Multi-PDF Chatbot using Groq, LangChain, FAISS, and Streamlit

This project is an AI-powered chatbot that allows users to upload multiple PDF documents and ask questions based on their contents. It leverages Groq's LLaMA 3 large language model, LangChain for RAG (Retrieval-Augmented Generation), FAISS for vector search, and Streamlit for the frontend.

## Features

- Upload multiple PDFs and interact with their content
- Real-time question answering based on PDF content
- Uses LangChain's RetrievalQA with FAISS vector store
- Powered by Groq's LLaMA 3 model for fast, high-quality responses
- Simple and interactive UI built with Streamlit

## Technologies Used

- LangChain
- Groq (LLaMA 3)
- FAISS (vector store)
- Hugging Face Sentence Transformers (embeddings)
- PyPDFLoader (for PDF parsing)
- Streamlit
- Python dotenv for environment variables

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/multi-pdf-chat.git
cd multi-pdf-chat
