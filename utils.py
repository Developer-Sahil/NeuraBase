import os
import fitz  # PyMuPDF for PDF parsing
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from docx import Document
import csv
import json

# Initialize Chroma client
CHROMA_DIR = "chroma_store"
os.makedirs(CHROMA_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="documents")

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def parse_pdf(file_path):
    """Extract text from a PDF using PyMuPDF."""
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text("text")
        if not text.strip():
            raise ValueError("No text extracted from PDF.")
        return text
    except Exception as e:
        raise ValueError(f"Error parsing PDF: {str(e)}")


def parse_txt(file_path):
    """Read text content from a .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Error reading TXT: {str(e)}")


def parse_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        if not text.strip():
            raise ValueError("No text extracted from DOCX.")
        return text
    except Exception as e:
        raise ValueError(f"Error parsing DOCX: {str(e)}")


def parse_csv(file_path):
    """Read and format CSV content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                raise ValueError("CSV file is empty.")
            # Format as readable text
            text = "\n".join([" | ".join(row) for row in rows])
            return text
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")


def parse_json(file_path):
    """Read and format JSON content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = json.dumps(data, indent=2)
            return text
    except Exception as e:
        raise ValueError(f"Error parsing JSON: {str(e)}")


def ingest_document(file_path):
    """Extract text, create embeddings, and store in ChromaDB."""
    ext = os.path.splitext(file_path)[-1].lower()

    # Parse based on file type
    if ext == ".pdf":
        text = parse_pdf(file_path)
    elif ext == ".txt":
        text = parse_txt(file_path)
    elif ext == ".docx":
        text = parse_docx(file_path)
    elif ext == ".csv":
        text = parse_csv(file_path)
    elif ext == ".json":
        text = parse_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Only PDF, TXT, DOCX, CSV, and JSON allowed.")

    if not text.strip():
        raise ValueError("No content could be extracted from the file.")

    # Create chunks with overlap for better context
    chunk_size = 500
    overlap = 50
    chunks = []
    
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    
    if not chunks:
        raise ValueError("No valid text chunks created from document.")

    # Generate embeddings
    embeddings = embedding_model.encode(chunks).tolist()

    # Create unique IDs for each chunk
    base_name = os.path.basename(file_path)
    ids = [f"{base_name}_chunk_{i}" for i in range(len(chunks))]
    
    # Add metadata
    metadatas = [{"source": base_name, "chunk_id": i} for i in range(len(chunks))]

    # Store in ChromaDB
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    return f"Successfully ingested {len(chunks)} chunks from {base_name}"


def search_documents(query, top_k=3):
    """Retrieve top-k relevant text chunks from ChromaDB."""
    if not query or not query.strip():
        return []
    
    try:
        query_embedding = embedding_model.encode([query]).tolist()
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        if not results or not results.get("documents"):
            return []

        # Flatten the results (ChromaDB returns nested lists)
        documents = [doc for sublist in results["documents"] for doc in sublist]
        return documents
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []


def get_collection_stats():
    """Get statistics about the document collection."""
    try:
        count = collection.count()
        return {"total_chunks": count}
    except Exception as e:
        return {"error": str(e)}