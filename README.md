# 🧠 NeuraBase — AI-Powered Knowledge Search Engine

**NeuraBase** is a Retrieval-Augmented Generation (RAG) system that lets you upload your documents and ask questions in natural language. The system retrieves relevant content and generates AI-powered answers — fast, intuitive, and intelligent.

---

## ✨ Features

* 📁 **Multi-format Uploads:** Supports PDF, TXT, DOCX, CSV, and JSON
* 🔍 **Semantic Search:** Uses sentence-transformers for intelligent retrieval
* 💾 **Persistent Storage:** Built on ChromaDB for efficient vector storage
* 🤖 **AI Responses:** Powered by Google’s Gemini API
* 🎨 **Modern UI:** Clean, responsive interface with a dynamic starry background
* ⚡ **Fast Processing:** Optimized text chunking and embedding
* 🔄 **Drag & Drop:** Simple, intuitive file upload experience

---

## 🚀 Quick Start

### Prerequisites

* Python 3.8 or higher
* Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd NeuraBase

# Create a virtual environment
python -m venv .venv

# Activate the environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run the Application

```bash
python app.py
```

Then open your browser and visit:
👉 [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
NeuraBase/
├── app.py              # Main Flask app and routes
├── utils.py            # Document processing and database utilities
├── llm.py              # LLM (Gemini API) integration
├── index.html          # Frontend UI
├── requirements.txt    # Dependencies
├── .env                # Environment variables
├── uploads/            # Uploaded files (auto-created)
└── chroma_store/       # Vector database (auto-created)
```

---

## ⚙️ How It Works

1. **Upload Documents** — Drop or select your files
2. **Extract Text** — Automatically reads and parses the content
3. **Chunk Content** — Splits text into smaller, meaningful sections
4. **Generate Embeddings** — Creates vector representations using `all-MiniLM-L6-v2`
5. **Store in ChromaDB** — Embeddings are indexed for quick retrieval
6. **Query with AI** — Your question is matched, and Gemini AI generates a response

---

## 🎯 Usage

### Uploading Documents

* Drag and drop or click to select files
* Supports multiple files and formats (PDF, TXT, DOCX, CSV, JSON)
* Click **Upload & Process** to build your knowledge base

### Asking Questions

* Type your question in the input box
* Adjust results (1–10) for better precision
* Press **Ctrl + Enter** or click **Search Knowledge Base**
* Get an AI-generated answer with source references

---

## 🧩 Key Components

### **Vector Database (ChromaDB)**

* Stores embeddings for fast semantic search
* Automatically manages collections and persistence

### **Sentence Transformers**

* Model: `all-MiniLM-L6-v2`
* Produces compact 384-dimensional embeddings

### **Gemini AI**

* Understands natural queries
* Generates clear, concise responses with context

---

## 🐛 Recent Fixes & Improvements

### **Backend Fixes**

* Updated routes (`/ask` → `/query`)
* Fixed multi-file uploads
* Integrated ChromaDB utilities with Flask routes
* Enhanced error handling and file validation

### **UI/UX Enhancements**

* Gradient backgrounds with glassmorphism design
* Drag & drop upload area
* Visual loading indicators
* Source citations for transparency
* Keyboard shortcuts (`Ctrl + Enter`)
* File preview with icons
* Fully responsive design

---

## 📊 API Endpoints

### **POST /upload**

Upload and process documents
**Request:** `FormData` with `files[]`
**Response:**

```json
{
  "success": ["file1.pdf", "file2.txt"],
  "errors": [],
  "total_uploaded": 2
}
```

### **POST /query**

Query the knowledge base
**Request:**

```json
{
  "query": "What is machine learning?",
  "top_k": 3
}
```

**Response:**

```json
{
  "answer": "Machine learning is ...",
  "sources": ["file1.pdf", "file2.txt"],
  "num_sources": 3
}
```

### **GET /health**

Check service status
**Response:**

```json
{
  "status": "healthy",
  "service": "NeuraBase RAG Engine"
}
```

---

## 🔧 Configuration

| Setting                                 | File     | Description            |
| --------------------------------------- | -------- | ---------------------- |
| `chunk_size = 500`                      | utils.py | Characters per chunk   |
| `overlap = 50`                          | utils.py | Overlap between chunks |
| `embedding_model = "all-MiniLM-L6-v2"`  | utils.py | Embedding model        |
| `MAX_CONTENT_LENGTH = 16 * 1024 * 1024` | app.py   | Max upload size (16MB) |

---

## 🔒 Security Notes

* Validates file types before processing
* Uses `secure_filename` for safe uploads
* API keys stored in `.env` (never committed)
* Sanitized query handling to prevent injection

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch

   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes

   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. Push and open a Pull Request

---

## 📝 License

Licensed under the **MIT License**.

---

## 🙏 Acknowledgments

* [ChromaDB](https://www.trychroma.com/) — Vector Database
* [Sentence Transformers](https://www.sbert.net/) — Embedding Models
* [Google Gemini](https://aistudio.google.com/) — AI Model
* [Flask](https://flask.palletsprojects.com/) — Web Framework

---

### 💡 Built by **Sahil Sharma**

Powered by **Flask**, **ChromaDB**, and **Gemini AI**.