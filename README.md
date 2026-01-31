## Description
LocalRAG is a fully local Retrieval‑Augmented Generation (RAG) application built with FastAPI, FAISS, and Ollama, designed to let users upload PDFs, index their contents, and ask natural‑language questions about the material. The system extracts text from documents, chunks it, embeds it using a local LLM, and performs similarity search through FAISS to retrieve the most relevant information. A lightweight frontend provides a clean chat interface for interacting with the knowledge base.

Created as a learning project focused on backend architecture, vector search, and local LLM integration, LocalRAG demonstrates how modern AI components—embeddings, retrieval, and generation—can be combined into a cohesive, fully offline pipeline. The project emphasizes clarity, modularity, and reproducibility, making it ideal for showcasing practical RAG implementation skills.

## Functionality
When the application starts, users can upload one or more PDF documents through the frontend interface. The backend processes each file by extracting text, chunking it into manageable segments, generating embeddings using an Ollama‑powered model, and storing them inside a FAISS index.

Once the knowledge base is populated, users can ask questions through the chat interface. The system retrieves the most relevant chunks using vector similarity search, feeds them into the LLM along with the user’s query, and returns a synthesized answer with contextual grounding. A reset option allows users to clear the index and start fresh at any time.

The entire workflow runs locally, ensuring privacy, speed, and zero dependency on paid APIs.

## Objective
The primary objective of this project was to gain experience with RAG architecture, vector databases, and local LLM inference. Rather than focusing on model training or UI design, the project focuses on understanding how retrieval pipelines work end-to-end and how different components interact to produce grounded, context-aware responses.

---

## Key Technical Areas

### Document Processing & Chunking
- Extracting text from PDFs using Python libraries  
- Splitting documents into semantically meaningful chunks  
- Managing chunk metadata for retrieval and citation  

---

### Embeddings & Vector Search
- Generating embeddings using an Ollama-powered model  
- Building and maintaining a FAISS index for similarity search  
- Persisting and reloading vector data across sessions  

---

### RAG Pipeline Construction
- Retrieving top-k relevant chunks based on cosine similarity  
- Constructing prompts that combine user queries with retrieved context  
- Generating grounded answers using a local LLM (Ollama in this case)

---

### Backend Architecture (FastAPI)
- Modular API endpoints for:
  - Upload
  - Query
  - Reset
- Handling CORS, file uploads, and JSON responses  
- Ensuring reproducibility and predictable behavior across runs  

---

### Frontend Integration
- Building a simple chat interface with **HTML/CSS/JavaScript**  
- Connecting the UI to backend endpoints via `fetch` requests  
- Displaying responses, citations, and system messages cleanly  

---

### Local LLM Execution (Ollama)
- Running inference fully **offline**  
- Managing model selection and embedding generation  
- Ensuring compatibility with FAISS vector dimensions  

---

## 🛠️ Installation

### Download the Project
- Click the Code button on the repository page and select **Download ZIP**
- Extract the contents to a folder of your choice

---

### Install Ollama
Download from:  
 https://ollama.com/download  

Then pull a model (example): ollama pull mistral

---

### Set Up the Python Environment
Create a virtual environment: python -m venv venv
Activate it for Windows: venv\Scripts\activate
Activate it for MacOS/Linux: source venv/bin/activate
Install dependencies: pip install -r requirements.txt

---
### Run the application
Double click on the file "run.bat" which is in the project root. This will launch the backend and frontend.

---
### Important
Ollama must be installed for the project to run.

All inference is performed locally—no API keys or paid services required.

The FAISS index is created automatically after uploading your first PDF.

If the index becomes corrupted or empty, simply reset the knowledge base.
