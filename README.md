# Chat Bot - AI-Powered Question Answering System

An intelligent chat bot that answers user questions by retrieving relevant context from a knowledge base and refining answers using AI.

##  Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system with the following architecture:

1. **Chroma.py** - Vector database for semantic search
2. **Chat_filter.py** - AI answer refinement using Groq API
3. **main.py** - Flask backend server
4. **Static files** - Frontend UI (HTML, CSS, JavaScript)

##  Data Flow

```
User Query
    ↓
main.py (Flask Server)
    ↓
Chroma.py (Vector DB Search)
    ↓ Retrieve Context Documents
Chat_filter.py (Groq API Refinement)
    ↓ Generate Refined Answer
main.py (Return Response)
    ↓
UI Display
```

##  Project Structure

```
Server/
├── main.py                 # Flask backend & API endpoints
├── Chroma.py              # Vector database operations
├── Chat_filter.py         # AI-powered answer refinement
├── requirement.txt        # Python dependencies
├── README.md             # This file
├── data/
│   ├── Contact.csv       # Contact information
│   └── data.txt          # Knowledge base content
├── chroma_db/            # Vector database storage
│   └── *.sqlite3         # Database files
├── static/
│   ├── style.css         # Frontend styling
│   └── script.js         # Frontend logic
└── templates/
    └── index.html        # Main UI page
```

##  Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Groq API key (get it from https://console.groq.com)

### step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/chat-bot.git
cd chat-bot/Server
```

### step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirement.txt
```

### Step 4: Configure Environment

Create a `.env` file in the Server directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Step 3: Prepare Knowledge Base

Ensure `data/data.txt` contains your knowledge base content. The system will:
- Split content into paragraphs
- Create vector embeddings using SentenceTransformer
- Store in ChromaDB for semantic search

##  How It Works

### 1. **Chroma.py** - Vector Database Search
- Uses `all-MiniLM-L6-v2` for embedding generation
- Stores documents in ChromaDB
- Retrieves top 3 most relevant documents for any query

```python
docs = query_collection("What is the policy?", n_results=3)
```

### 2. **Chat_filter.py** - Answer Refinement
- Takes user question + retrieved context
- Sends to Groq API (llama-3.1-8b-instant model)
- Generates a focused, contextual answer
- Returns refined response (keeps original context intact)

```python
refined_answer = refine_answer(question, context_docs)
```

### 3. **main.py** - API Server
- Flask backend with two routes:
  - `GET /` - Serves UI
  - `POST /api/query` - Receives questions and returns answers
- Orchestrates the entire flow

### 4. **Frontend (UI)**
- Located in `templates/index.html`
- Real-time chat interface
- Displays refined AI answers
- Handles loading states and errors

##  Usage

### Start the Server

```bash
python main.py
```

Server runs on: `http://localhost:5000`

### Access UI

Open your browser and go to:
```
http://localhost:5000
```

### Running in Terminal (Debug Mode)

```bash
python Chroma.py
```

This allows you to query the vector database directly for testing.

##  Configuration

### Embedding Model
- **Model**: `all-MiniLM-L6-v2` (lightweight, efficient)
- **Location**: `Chroma.py` line 8

### LLM Model
- **Provider**: Groq
- **Model**: `llama-3.1-8b-instant` (fast, high-quality)
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 1024

To change the LLM model, edit `Chat_filter.py`:
```python
model="llama-3.1-8b-instant",  
```

### Search Results
- **Number of results**: 3 documents
- **Location**: `main.py` line 23


##  Example Usage

**User Query**: "What are the contact policies?"

**Process**:
1. Query sent to `/api/query`
2. Chroma retrieves 3 most similar documents
3. Chat_filter refines using Groq AI
4. Response shows AI-generated answer with context

**Sample Response**:
```
Answer: "Contact policies include... [refined by AI based on your knowledge base]"
```

##  Security Notes

- Store `GROQ_API_KEY` in `.env` file (add to `.gitignore`)
- Don't commit `.env` to version control
- API key provides access to Groq services (monitor usage)

##  Tips for Best Results

1. **Quality Data**: Ensure `data/data.txt` has clear, well-organized content
2. **Paragraph Chunking**: Content is split by double line breaks - organize accordingly
3. **Testing Queries**: Test with simple queries first, then complex ones
4. **Monitor API Usage**: Check Groq console for usage statistics

##  Contributing

To improve the system:
1. Add better context documents in `data/data.txt`
2. Experiment with different embedding models
3. Test with various question types
4. Optimize temperature and token settings

##  License

any one can use

##  Author

develop by devloper

---

**Last Updated**: April 2, 2026
**Version**: 1.0.0
