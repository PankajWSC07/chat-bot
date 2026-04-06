# LangChain Chatbot

A Flask-based chatbot application that uses LangChain and ChromaDB for retrieval-augmented generation (RAG).

## Features

- Document loading and chunking from text files
- Vector embeddings using Hugging Face models
- Semantic search with ChromaDB
- Web interface for user queries
- Response filtering and improvement

## Project Structure

```
├── main.py              # Flask application entry point
├── LangChain.py         # Vector database and retrieval logic
├── Chat_filter.py       # Response filtering and improvement
├── data/                # Data files for RAG│ 
│   └── data1.txt
├── templates/           # HTML templates
│   └── index.html
├── static/              # CSS and JavaScript files
│   ├── style.css
│   └── script.js
└── requirement.txt      # Python dependencies
```

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   on macOS/Linux
.venv\Scripts\activate      on Windows 
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

3. Configure Environment

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

4. Prepare Knowledge Base

Ensure `data/data.txt` contains your knowledge base content. The system will:
- Split content into paragraphs
- Create vector embeddings using SentenceTransformer
- Store in ChromaDB for semantic search

## Usage

Run the Flask application:
```bash
python main.py
```
The application will start on `http://localhost:5000`

Running in Terminal (Debug Mode)

```bash
python LangChain.py
```


## How It Works

1. **Data Loading**: Text files from `data/` directory are loaded and split into paragraphs
2. **Embeddings**: Paragraphs are converted to vector embeddings using Hugging Face models
3. **Storage**: Vectors are stored in ChromaDB for fast retrieval
4. **Retrieval**: User queries retrieve relevant documents from the vector store
5. **Response**: Retrieved context is used to improve the chatbot's answer

## Requirements

See `requirement.txt` for all dependencies.


