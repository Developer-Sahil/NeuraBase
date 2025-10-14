from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from utils import ingest_document, search_documents
from llm import call_llm_api

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'csv', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle multiple file uploads and ingest into vector DB"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    results = []
    errors = []
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Ingest into vector database
                result = ingest_document(filepath)
                results.append({
                    'filename': filename,
                    'status': 'success',
                    'message': result
                })
            except Exception as e:
                errors.append({
                    'filename': file.filename,
                    'status': 'error',
                    'message': str(e)
                })
        else:
            errors.append({
                'filename': file.filename,
                'status': 'error',
                'message': 'Invalid file type. Allowed: pdf, txt, docx, csv, json'
            })
    
    return jsonify({
        'success': results,
        'errors': errors,
        'total_uploaded': len(results)
    })


@app.route('/query', methods=['POST'])
def query_documents():
    """Query the knowledge base and generate answer"""
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        question = data.get('query', '').strip()
        top_k = int(data.get('top_k', 3))
        
        if not question:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Search vector database for relevant chunks
        relevant_docs = search_documents(question, top_k=top_k)
        
        if not relevant_docs:
            return jsonify({
                'answer': 'I could not find any relevant information in the knowledge base to answer your question. Please try rephrasing or upload relevant documents.',
                'sources': []
            })
        
        # Combine context from retrieved documents
        context = "\n\n".join(relevant_docs)
        
        # Generate answer using LLM
        answer = call_llm_api(question, context)
        
        return jsonify({
            'answer': answer,
            'sources': relevant_docs[:3],  # Return top 3 sources
            'num_sources': len(relevant_docs)
        })
    
    except Exception as e:
        return jsonify({'error': f'Query processing error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'NeuraBase RAG Engine'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)