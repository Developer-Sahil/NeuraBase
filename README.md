# 🧠 NeuraBase - AI-Powered Knowledge Search Engine

A powerful Retrieval-Augmented Generation (RAG) system that allows you to upload documents and query them using natural language with AI-powered responses.

![NeuraBase](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

## ✨ Features

- 📁 **Multi-format Support**: Upload PDF, TXT, DOCX, CSV, and JSON files
- 🔍 **Semantic Search**: Uses sentence-transformers for intelligent document retrieval
- 💾 **Persistent Storage**: ChromaDB vector database for efficient storage and retrieval
- 🤖 **AI Responses**: Powered by Google's Gemini API for intelligent answers
- 🎨 **Modern UI**: Beautiful, responsive interface with animated starry background
- ⚡ **Fast Processing**: Efficient chunking and embedding generation
- 🔄 **Drag & Drop**: Intuitive file upload with drag-and-drop support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd NeuraBase
```

2. **Create virtual environment**
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
NeuraBase/
├── app.py              # Flask application and routes
├── utils.py            # Document processing and vector DB utilities
├── llm.py             # LLM integration (Gemini API)
├── index.html         # Frontend UI
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
├── uploads/          # Uploaded files (auto-created)
└── chroma_store/     # Vector database (auto-created)
```

## 🔧 How It Works

1. **Document Upload**: Files are uploaded and parsed based on their format
2. **Text Extraction**: Content is extracted using format-specific parsers
3. **Chunking**: Text is split into manageable chunks (500 chars with 50 char overlap)
4. **Embedding**: Each chunk is converted to a vector using `all-MiniLM-L6-v2` model
5. **Storage**: Embeddings are stored in ChromaDB for fast retrieval
6. **Query**: User questions are embedded and matched against stored chunks
7. **Response**: Relevant context is sent to Gemini AI for answer generation

## 🎯 Usage

### Uploading Documents

1. Click the upload area or drag files directly
2. Select one or multiple files (PDF, TXT, DOCX, CSV, JSON)
3. Click "Upload & Process" to ingest into the knowledge base

### Asking Questions

1. Type your question in the query box
2. Adjust the number of results to retrieve (1-10)
3. Click "Search Knowledge Base" or press Ctrl+Enter
4. View AI-generated answer with source references

## 🔑 Key Features Explained

### Vector Database (ChromaDB)
- Persistent storage of document embeddings
- Fast similarity search for relevant content
- Automatic collection management

### Sentence Transformers
- `all-MiniLM-L6-v2` model for embeddings
- Efficient semantic understanding
- 384-dimensional vectors

### Gemini AI Integration
- Contextual answer generation
- Natural language understanding
- Concise and accurate responses

## 🐛 Debugging Changes Made

### Fixed Issues:

1. **Route Mismatch**: Changed `/ask` to `/query` to match frontend
2. **File Handling**: Fixed multiple file upload (changed from `file` to `files`)
3. **Template Path**: Using `send_from_directory` instead of `render_template`
4. **Integration**: Connected ChromaDB utilities to Flask routes
5. **Error Handling**: Added comprehensive try-catch blocks
6. **File Type Support**: Extended parsing for DOCX, CSV, JSON
7. **Dependencies**: Updated requirements.txt with all needed packages

### UI/UX Improvements:

1. **Modern Design**: Gradient backgrounds, glassmorphism effects
2. **Drag & Drop**: Intuitive file upload interface
3. **Loading States**: Visual feedback during operations
4. **Error Messages**: Clear, user-friendly error displays
5. **Responsive Layout**: Works on mobile and desktop
6. **Source Citations**: Shows relevant document chunks
7. **Keyboard Shortcuts**: Ctrl+Enter to submit query
8. **File Preview**: Display uploaded files with icons

## 📊 API Endpoints

### POST `/upload`
Upload and process documents
```json
Request: FormData with 'files' array
Response: {
  "success": [...],
  "errors": [...],
  "total_uploaded": 2
}
```

### POST `/query`
Query the knowledge base
```json
Request: {
  "query": "What is...",
  "top_k": 3
}
Response: {
  "answer": "...",
  "sources": [...],
  "num_sources": 3
}
```

### GET `/health`
Health check endpoint
```json
Response: {
  "status": "healthy",
  "service": "NeuraBase RAG Engine"
}
```

## ⚙️ Configuration

### Chunk Settings (in utils.py)
```python
chunk_size = 500      # Characters per chunk
overlap = 50          # Overlap between chunks
```

### Model Settings (in utils.py)
```python
embedding_model = "all-MiniLM-L6-v2"  # Sentence transformer model
```

### Upload Limits (in app.py)
```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
```

## 🔒 Security Considerations

- File type validation before processing
- Secure filename handling with `werkzeug.secure_filename`
- Environment variables for API keys
- Input sanitization for queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - Embedding models
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM API
- [Flask](https://flask.palletsprojects.com/) - Web framework

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built by Sahil Sharma** • Powered by Flask, ChromaDB & Gemini AI