# MedReport AI

AI-powered medical lab report assistant built with Retrieval-Augmented Generation (RAG), FastAPI, and React.

MedReport AI processes uploaded medical PDF reports, extracts and validates lab metrics, retrieves reference medical knowledge via FAISS, and generates source-grounded explanations with safety checks.

> **Medical Disclaimer:** Intended for educational and informational purposes only. Not a medical diagnostic tool and must not replace professional medical advice, diagnosis, or treatment.

---

## Key Features

- **PDF Extraction & Parsing:** Extracts text with PyMuPDF, structures lab values, validates report integrity, and generates concise summaries.
- **Supported Lab Panels:** CBC, Glucose, Lipid Profile, Liver Function (LFT), Kidney Function (KFT), and Thyroid panels (PDF format).
- **Local Semantic Embeddings:** Encodes queries and reference documents into 384-dimensional vectors using `all-MiniLM-L6-v2` without external embedding API calls.
- **FAISS Vector Retrieval:** Performs similarity search over pre-indexed medical knowledge (`vectorstore/medical_knowledge.index`).
- **Multi-Turn Follow-Up Chat & Safety Guardrails:** Generates context-aware answers via Groq LLM and runs output safety verification before returning responses.

---

## System & RAG Architecture

### Application & Pipeline Architecture

```text
┌──────────────────────────────────────────────────────────────────────┐
│                        React + Vite Frontend                         │
│        PDF Report Upload  •  Report Summary  •  Follow-Up Chat       │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │ HTTPS / REST
┌──────────────────────────────────▼───────────────────────────────────┐
│                      FastAPI Application Layer                       │
│            GET /health   •   POST /analyze   •   POST /chat          │
└───────────┬──────────────────────┬──────────────────────┬────────────┘
            │                      │                      │
            ▼                      ▼                      ▼
┌───────────────────────┐ ┌─────────────────┐ ┌────────────────────────┐
│  Ingestion Pipeline   │ │   RAG Engine    │ │     Safety Layer       │
│  - PyMuPDF Extraction │ │ - MiniLM-L6-v2  │ │ - Response Guardrails  │
│  - Test Value Parser  │ │ - FAISS Search  │ │ - Medical Disclaimer   │
│  - Validator & Summary│ │ - Groq LLM API  │ │                        │
└───────────────────────┘ └─────────────────┘ └────────────────────────┘
```

### Offline Indexing & Online Query Flow

```text
[Offline Knowledge Indexing]
Medical Knowledge ──► LangChain Splitter ──► all-MiniLM-L6-v2 (384-d) ──► FAISS Index (.index + .pkl)

[Online Query & Response]
Uploaded PDF ──► PyMuPDF Extract ──► Parser & Validator ──► Report Summary ─┐
                                                                            ├──► Groq LLM ──► Safety Check ──► Final Answer
User Question ──► all-MiniLM-L6-v2 (384-d) ──► FAISS Search ──► Context ────┘
```

### AWS Deployment Architecture

```text
                        Internet
                           │
                           ▼
                   Amazon CloudFront
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
     Static Frontend               Backend API
       (Amazon S3)                 (Amazon EC2)
                                         │
                             ┌───────────┼───────────┐
                             │           │           │
                             ▼           ▼           ▼
                      all-MiniLM-L6    FAISS      Groq API
```

---

## Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, JavaScript, Axios |
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **AI / RAG** | SentenceTransformers (`all-MiniLM-L6-v2`), FAISS, LangChain Text Splitters, Groq API |
| **Document Processing** | PyMuPDF (`fitz`) |
| **Deployment** | AWS (S3, CloudFront, EC2) |

---

## Project Structure & Backend Modules

```text
MedReport_AI/
├── backend/
│   ├── api/
│   │   └── main.py                 # REST endpoints (/health, /analyze, /chat)
│   ├── ingestion/
│   │   ├── pdf.py                  # PyMuPDF text extraction
│   │   ├── parser.py               # Structured lab metric parsing
│   │   ├── validator.py            # Report format & field validation
│   │   └── summary.py              # Report summary generation
│   ├── knowledge/
│   │   ├── documents.py            # Knowledge base document loader
│   │   ├── chunking.py             # Text splitting utilities
│   │   ├── embeddings.py           # SentenceTransformer (384-d) wrapper
│   │   └── vectorstore.py          # FAISS index creation & persistence
│   ├── retrieval/
│   │   ├── search.py               # FAISS similarity search
│   │   ├── test_matcher.py         # Lab test matching logic
│   │   ├── context.py              # Context assembly
│   │   └── context_formatter.py    # Prompt context formatting
│   ├── generation/
│   │   ├── prompts.py              # System & RAG prompt templates
│   │   ├── llm.py                  # Groq LLM integration
│   │   └── response.py             # Output structuring
│   ├── safety/
│   │   └── checker.py              # Response safety verification
│   ├── config.py                   # Centralized paths & RAG parameters
│   ├── models.py                   # Pydantic request/response schemas
│   └── pipeline.py                 # End-to-end RAG orchestration
├── data/
│   ├── knowledge_base/             # Reference medical knowledge documents
│   ├── processed/                  # Processed chunks & metadata
│   └── reports/temp/               # Transient uploaded report storage
├── vectorstore/
│   ├── medical_knowledge.index     # Pre-built FAISS vector index
│   └── knowledge_documents.pkl     # Serialized document chunks
├── frontend/
│   ├── src/App.jsx                 # React application root
│   ├── public/
│   └── package.json
├── tests/                          # Automated backend test suite
├── requirements.txt
├── .env.example
└── README.md
```

---

## API Reference

| Method | Endpoint | Content-Type | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | `application/json` | Service health check (`{"status": "healthy"}`) |
| `POST` | `/analyze` | `multipart/form-data` | Accepts `file` (PDF) and `question`; returns summary & grounded answer |
| `POST` | `/chat` | `application/json` | Handles follow-up questions against the active analysis session |

---

## Local Development Setup

### 1. Clone & Configure Environment
```bash
git clone [https://github.com/sk3026/MedReport_AI.git](https://github.com/sk3026/MedReport_AI.git)
cd MedReport_AI
cp .env.example .env
```
Add your Groq API key to `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Start the Backend
Run from the **repository root** (`MedReport_AI/`):
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (use `source .venv/bin/activate` on macOS/Linux)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn backend.api.main:app --reload --port 8000
```
API docs are available at `http://localhost:8000/docs`.

### 3. Start the Frontend
Open a second terminal from the repository root:
```bash
cd frontend
npm install
npm run dev
```
Open the app at `http://localhost:5173`.

---

## Production Build & Testing

- **Build Frontend:**
  ```bash
  cd frontend && npm run build   # Outputs static bundle to frontend/dist/
  ```
- **Run Production API:**
  ```bash
  python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
  ```
- **Run Tests & Health Check:**
  ```bash
  pytest
  curl http://localhost:8000/health
  ```

---

## Security & Data Handling

- **Transient Report Processing:** Uploaded PDFs in `data/reports/temp/` are excluded from version control and should be purged after session completion in production.
- **Sanitized Logging:** Operational logs capture request status and errors without recording patient identifiers, raw report text, or API keys.
- **Environment Isolation:** Secrets (`GROQ_API_KEY`, `VITE_API_URL`) are injected via environment variables and never committed to source control.