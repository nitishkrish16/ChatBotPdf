# -*- coding: utf-8 -*-
"""ChatBot_Hackathon.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QHUF_3gHD-bqV_ldKpIHnj20QeCXpFIm
"""

!pip install flask
!pip install flask-ngrok
!pip install sentence-transformers
!pip install pymupdf
!pip install faiss-cpu
!pip install groq
!pip install pyngrok
!pip install gradio

import gradio as gr
from groq import Groq
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
import faiss
import numpy as np

API_KEY = "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"

def extract_text(pdf_path):
    with fitz.open(pdf_path) as document:
        full_text = "".join([page.get_text("text") for page in document])
    return full_text

def partition_text(text, max_length=1000):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def compute_embeddings(text_segments, model_name='paraphrase-MiniLM-L6-v2'):
    transformer = SentenceTransformer(model_name)
    return transformer.encode(text_segments, convert_to_tensor=True), transformer

def build_faiss_index(embedding_vectors):
    vector_dimension = embedding_vectors.shape[1]
    faiss_index = faiss.IndexFlatL2(vector_dimension)
    faiss_index.add(embedding_vectors.cpu().numpy())
    return faiss_index

def search_similar_chunks(query_text, index, segments, transformer, num_results=3):
    query_vector = transformer.encode([query_text], convert_to_tensor=True)
    distances, indices = index.search(query_vector.cpu().numpy(), num_results)
    return [segments[idx] for idx in indices[0]]

def retrieve_pdf_context(pdf_path, user_query):
    document_text = extract_text(pdf_path)
    text_chunks = partition_text(document_text)
    embeddings, embedding_model = compute_embeddings(text_chunks)
    index = build_faiss_index(embeddings)
    return search_similar_chunks(user_query, index, text_chunks, embedding_model)

def query_pdf(pdf_file, user_query):
    pdf_path = pdf_file.name  # Use the uploaded file path
    retrieved_context = retrieve_pdf_context(pdf_path, user_query)

    context_text = "\n".join(retrieved_context)
    client = Groq(api_key=API_KEY)

    completion_response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": context_text + "\n" + user_query
        }],
        model="llama3-70b-8192"
    )

    return completion_response.choices[0].message.content

# Create Gradio interface
def create_ui():
    pdf_input = gr.File(label="Upload PDF", type="filepath")
    query_input = gr.Textbox(label="Enter Your Query", placeholder="Type your query here...")
    output = gr.Textbox(label="Groq Completion Response")

    interface = gr.Interface(
        fn=query_pdf,
        inputs=[pdf_input, query_input],
        outputs=output,
        title="PDF Query and Context Retrieval",
        description="Upload a PDF, enter a query, and retrieve relevant context and Groq response.",
    )

    return interface

# Run the Gradio app
create_ui().launch()