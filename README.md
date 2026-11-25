# MedReport AI

AI-powered medical report analysis using Retrieval-Augmented Generation (RAG).

MedReport AI is a full-stack application that processes medical PDF reports, retrieves relevant medical knowledge, and generates context-aware responses using a large language model.

The system is designed with a modular backend, React frontend, vector-based retrieval, and REST API architecture.

> **Medical Disclaimer:** MedReport AI is intended for educational and informational purposes. It is not a medical diagnostic system and should not be used as a substitute for professional medical advice.

---

## Overview

MedReport AI combines:

- Medical PDF processing
- Report validation
- Report summarization
- Semantic search
- Local vector embeddings
- FAISS vector retrieval
- Retrieval-Augmented Generation
- Large language model response generation
- Response safety checking
- React-based user interface
- FastAPI REST API

The system follows this general pipeline:

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI API
 │
 ├── PDF Processing
 │
 ├── Report Validation
 │
 ├── Report Summary
 │
 ├── Question Embedding
 │
 ├── FAISS Retrieval
 │
 ├── Context Preparation
 │
 ├── LLM Generation
 │
 └── Safety Check
 │
 ▼
Final Response
```

---

## Architecture

### Application Architecture

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                      ┌──────────────────┐
                      │ React Frontend   │
                      └────────┬─────────┘
                               │
                               │ HTTPS / REST
                               ▼
                      ┌──────────────────┐
                      │   FastAPI API    │
                      └────────┬─────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
         PDF Processing    RAG Pipeline   Safety Layer
                               │
                               ▼
                       ┌──────────────┐
                       │ Sentence     │
                       │ Transformer  │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │    FAISS     │
                       │ Vector Store │
                       └──────┬───────┘
                              │
                              ▼
                      Retrieved Context
                              │
                              ▼
                       ┌──────────────┐
                       │    LLM API   │
                       └──────┬───────┘
                              │
                              ▼
                       Generated Answer
```

---

## RAG Architecture

The application uses Retrieval-Augmented Generation instead of relying only on the LLM's pretrained knowledge.

### Knowledge Indexing

```text
Medical Knowledge
       │
       ▼
    Chunking
       │
       ▼
  Text Chunks
       │
       ▼
SentenceTransformer
       │
       ▼
  Embeddings
       │
       ▼
     FAISS
       │
       ▼
Vector Index
```

### Question Processing

```text
User Question
       │
       ▼
SentenceTransformer
       │
       ▼
Question Embedding
       │
       ▼
FAISS Similarity Search
       │
       ▼
Relevant Knowledge
       │
       ▼
Context
```

### Response Generation

```text
User Question
      +
Uploaded Report Context
      +
Retrieved Medical Knowledge
      │
      ▼
     LLM
      │
      ▼
Safety Check
      │
      ▼
Final Response
```

---

## Technology Stack

### Frontend
- React
- Vite
- JavaScript
- Axios

### Backend
- Python
- FastAPI
- Uvicorn

### AI / RAG
- SentenceTransformers (`all-MiniLM-L6-v2`)
- FAISS
- LangChain text splitters
- Groq API

### Document Processing
- PyMuPDF



## Project Structure

```text
MedReport_AI/
│
├── backend/
│   ├── api/
│   │   └── main.py
│   │
│   ├── ingestion/
│   │   ├── parser.py
│   │   ├── pdf.py
│   │   ├── summary.py
│   │   └── validator.py
│   │
│   ├── knowledge/
│   │   ├── chunking.py
│   │   ├── documents.py
│   │   ├── embeddings.py
│   │   └── vectorstore.py
│   │
│   ├── retrieval/
│   │   ├── search.py
│   │   ├── context.py
│   │   ├── context_formatter.py
│   │   └── test_matcher.py
│   │
│   ├── generation/
│   │   ├── llm.py
│   │   ├── prompts.py
│   │   └── response.py
│   │
│   ├── safety/
│   │   └── checker.py
│   │
│   ├── config.py
│   ├── models.py
│   └── pipeline.py
│
├── data/
│   ├── knowledge_base/
│   ├── processed/
│   └── reports/
│       └── temp/
│
├── vectorstore/
│   ├── medical_knowledge.index
│   └── knowledge_documents.pkl
│
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   └── dist/
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── package.json
```

---

## Backend Modules

### API (`backend/api/`)
Exposes the application's REST endpoints (`main.py`) and connects the frontend with the processing pipeline.

### Ingestion (`backend/ingestion/`)
Processes uploaded medical PDF reports through extraction, parsing, validation, and summary generation.

### Knowledge (`backend/knowledge/`)
Prepares and manages medical reference documents via chunking, embedding generation, and FAISS vectorstore management.

### Retrieval (`backend/retrieval/`)
Performs semantic similarity search from the FAISS vector index and formats matched lab test chunks into prompt context.

### Generation (`backend/generation/`)
Communicates with the Groq LLM using the user question, parsed report context, retrieved medical knowledge, and prompt templates.

### Safety (`backend/safety/`)
Checks generated responses against safety guardrails before returning them to the client.

---

## Embeddings & Vector Store

- **Embedding Model:** `all-MiniLM-L6-v2` (384-dimensional vectors) running locally inside the backend environment without an external embedding API.
- **Vector Store:** FAISS similarity search over:
  ```text
  vectorstore/
  ├── medical_knowledge.index
  └── knowledge_documents.pkl
  ```

---

## Supported Reports

- CBC
- Glucose
- Lipid Profile
- Liver Function
- Kidney Function
- Thyroid

Supported upload format: `PDF`



## Local Development

### Backend

1. Create and activate a virtual environment from the repository root:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows (use `source .venv/bin/activate` on macOS/Linux)
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the API:
   ```bash
   python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Production Build & Deployment

### Build Frontend
```bash
cd frontend
npm run build
```
Static production files are generated in `frontend/dist/`.

### Start Backend
```bash
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### AWS Deployment Architecture

```text
                         Internet
                            │
                            ▼
                     CloudFront
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
         Static Frontend             Backend API
              │                           │
              ▼                           ▼
             S3                         EC2
                                          │
                              ┌───────────┼───────────┐
                              │           │           │
                              ▼           ▼           ▼
                       Embedding Model   FAISS      LLM API
```

---

## Configuration

Application settings are centralized in `backend/config.py`, including data/knowledge-base paths, vectorstore location, chunk size/overlap, retrieval count, supported report types, and file formats.

---

## Testing & Monitoring

Run backend tests:
```bash
pytest
```

Verify API health:
```bash
curl http://localhost:8000/health
```

---

## Security & Data Handling

- **Transport & Secrets:** Use HTTPS in production and inject API keys via environment variables rather than source control.
- **Transient Uploads:** Avoid unnecessary persistence of uploaded reports in `data/reports/temp/` and restrict file access.
- **Sanitized Logging:** Log operational events (`Request received`, `Request completed`, `Processing failed`, `External API failure`) without logging patient names, medical record numbers, raw report text, or API keys.

---

## Development vs Production

| Area | Development | Production |
| :--- | :--- | :--- |
| Frontend | Vite development server | Production static build |
| Backend | Uvicorn (`--reload`) | Uvicorn / production server |
| Configuration | `.env` | Secure environment variables |
| HTTPS | Optional | Required |
| Logs | Console | Centralized logging |
| Storage | Local | Managed storage where required |
| Scaling | Single instance | Multiple instances if required |
| Monitoring | Basic | Application and infrastructure monitoring |
| Secrets | Local environment | Secure secret management |

---

## Future Enhancements

- User authentication and authorization
- Persistent conversation and secure report storage
- Streaming responses and RAG citations
- Additional medical report formats and improved extraction
- Retrieval evaluation and automated CI/CD

---

## Medical Disclaimer

MedReport AI provides AI-generated informational responses based on uploaded documents and retrieved knowledge. It is not intended to diagnose medical conditions, prescribe medication, replace healthcare professionals, or make clinical decisions. Users should consult a qualified healthcare professional for medical diagnosis and treatment.

---

## License

MIT License

---

## Author

**MedReport AI** — AI-powered medical report analysis and RAG application.