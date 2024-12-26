# 📄 Smart PDF Chatbot for Context-Based Document Queries

A chatbot system designed to retrieve accurate, fact-based responses from uploaded PDF documents using advanced AI techniques. This project uses a combination of Large Language Models (LLMs), FAISS indexing, and secure REST APIs to deliver fast and reliable answers directly referenced from source material.

---

## 🚀 Features

- **PDF Ingestion**: Upload and process PDF files to extract text.
- **Contextual Query Handling**: Retrieve relevant sections of the document to answer user queries.
- **Accurate Responses**: Ensures all responses are grounded in the provided documents to prevent hallucinations.
- **Interactive UI**: Simple and intuitive user interface built using Gradio.
- **Scalable Backend**: REST API architecture with efficient query processing.
- **Future Enhancements**:
  - Bulk PDF uploads
  - Improved security (e.g., encryption and role-based access control)
  - Real-time streaming APIs for better user experience

---

## 🛠️ Tech Stack

### Backend
- **Python**: Core programming language.
- **PyMuPDF (`fitz`)**: For PDF text extraction.
- **SentenceTransformers**: For embedding generation.
- **FAISS**: For similarity search and indexing.
- **Groq API**: To interface with LLMs for generating responses.

### Frontend
- **Gradio**: For creating a user-friendly web interface.

---
