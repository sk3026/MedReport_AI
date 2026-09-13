# MedReport AI

AI-powered medical report analysis using Retrieval-Augmented Generation (RAG).

MedReport AI is a full-stack application that processes medical PDF reports,
retrieves relevant medical knowledge, and generates context-aware responses
using a large language model.

The system is designed with a modular backend, React frontend, vector-based
retrieval, and REST API architecture.

> **Medical Disclaimer:** MedReport AI is intended for educational and
> informational purposes. It is not a medical diagnostic system and should
> not be used as a substitute for professional medical advice.

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

# Architecture

## Application Architecture

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

# RAG Architecture

The application uses Retrieval-Augmented Generation instead of relying
only on the LLM's pretrained knowledge.

## Knowledge Indexing

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

## Question Processing

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

## Response Generation

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

# Technology Stack

## Frontend

- React
- Vite
- JavaScript
- Axios

## Backend

- Python
- FastAPI
- Uvicorn

## AI / RAG

- SentenceTransformers
- `all-MiniLM-L6-v2`
- FAISS
- LangChain text splitters
- Groq API

## Document Processing

- PyMuPDF

## Deployment

- AWS
- Amazon S3
- Amazon CloudFront
- Amazon EC2

---

# Project Structure

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

# Backend Modules

## API

Location:

```text
backend/api/
```

The API layer exposes the application's REST endpoints and connects the
frontend with the processing pipeline.

Main file:

```text
main.py
```

---

## Ingestion

Location:

```text
backend/ingestion/
```

Responsible for processing uploaded medical reports.

```text
PDF
 │
 ├── Extract
 ├── Parse
 ├── Validate
 └── Summarize
```

Main components:

- PDF extraction
- Report parsing
- Report validation
- Summary generation

---

## Knowledge

Location:

```text
backend/knowledge/
```

Responsible for preparing and managing the medical knowledge used by the
RAG pipeline.

Responsibilities include:

- Document processing
- Chunking
- Embedding generation
- Vectorstore management

---

## Retrieval

Location:

```text
backend/retrieval/
```

Responsible for semantic retrieval from the FAISS vector index.

The retrieval pipeline is:

```text
Question
   │
   ▼
Embedding
   │
   ▼
FAISS Search
   │
   ▼
Relevant Chunks
   │
   ▼
Context
```

---

## Generation

Location:

```text
backend/generation/
```

Responsible for communicating with the LLM and generating the final
response.

The LLM receives:

- User question
- Report context
- Retrieved medical knowledge
- Prompt instructions

---

## Safety

Location:

```text
backend/safety/
```

Responsible for checking generated responses before they are returned
to the client.

---

# Embeddings

The system uses:

```text
all-MiniLM-L6-v2
```

for semantic embeddings.

Embedding dimension:

```text
384
```

The embedding model runs within the backend environment.

This means the application does not require a separate embedding API for
question and knowledge-vector generation.

```text
Text
 │
 ▼
all-MiniLM-L6-v2
 │
 ▼
384-Dimensional Vector
 │
 ▼
FAISS
```

---

# Vector Store

FAISS is used for semantic similarity search.

The vector index consists of:

```text
vectorstore/
├── medical_knowledge.index
└── knowledge_documents.pkl
```

The retrieval configuration uses a configurable number of relevant
documents or chunks.

---

# Supported Reports

The current application is configured to support medical report categories
including:

- CBC
- Glucose
- Lipid Profile
- Liver Function
- Kidney Function
- Thyroid

Supported upload format:

```text
PDF
```

---

# API

## Base URL

The API base URL is environment-dependent.

Local:

```text
http://localhost:8000
```

Production:

```text
https://<your-production-domain>
```

---

## Endpoints

### Health Check

```http
GET /health
```

Used to verify that the API is available.

Example response:

```json
{
  "status": "healthy"
}
```

---

### Analyze Report

```http
POST /analyze
```

Processes a medical report and answers the initial user question.

Request:

```text
multipart/form-data
```

Fields:

```text
file
question
```

---

### Chat

```http
POST /chat
```

Processes follow-up questions for an existing analysis session.

---

# Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

Frontend production configuration:

```env
VITE_API_URL=https://<your-production-domain>
```

Do not commit `.env` to source control.

---

# Local Development

## Backend

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

---

## Frontend

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the URL shown by Vite.

---

# Production Build

Build the frontend:

```bash
cd frontend
npm run build
```

The production files are generated in:

```text
frontend/dist/
```

The production frontend can be served through a static hosting service
or web server.

The backend can be started using:

```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

---

# Deployment

The application consists of a React frontend and a FastAPI backend.

The frontend is built as a production static application and can be served
using a static hosting service or web server.

The backend runs using Uvicorn and exposes the FastAPI REST API.

A production deployment should use HTTPS and secure environment-variable
management.

The application is designed to be deployable on cloud infrastructure.

---

# AWS Deployment Architecture

A production AWS deployment can follow this architecture:

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

The frontend is hosted as a static application.

The backend runs as a FastAPI application.

The frontend communicates with the backend through the configured API
base URL.

---

# Production Configuration

Production deployments should use:

```text
HTTPS
 │
 ▼
Frontend / CDN
 │
 ▼
Backend API
 │
 ├── Embedding Model
 │
 ├── FAISS Vectorstore
 │
 └── LLM API
```

The backend should listen on:

```text
0.0.0.0:8000
```

Environment-specific configuration should be supplied through environment
variables.

---

# Security

The application handles potentially sensitive medical information.

Production deployments should implement appropriate security controls.

Recommended controls include:

- HTTPS
- Authentication
- Authorization
- Secure secret management
- Encryption in transit
- Encryption at rest
- Strict file validation
- File-size limits
- Rate limiting
- Secure temporary file handling
- Access logging
- Audit logging
- Monitoring
- Controlled data retention
- Secure deletion of temporary data

API credentials must never be committed to source control.

---

# Data Handling

Uploaded reports may contain sensitive information.

Production deployments should:

- Minimize data retention.
- Avoid unnecessary persistence of uploaded reports.
- Restrict access to uploaded files.
- Encrypt stored data.
- Define retention and deletion policies.
- Prevent sensitive information from appearing in application logs.
- Avoid including patient information in error messages.
- Avoid uploading patient data to public repositories.

---

# Configuration

Application configuration is centralized through:

```text
backend/config.py
```

Configuration includes items such as:

- Data directories
- Knowledge-base directories
- Vectorstore location
- Chunk size
- Chunk overlap
- Retrieval count
- Supported report types
- Supported file formats

Environment-specific values should be supplied through environment variables
where appropriate.

---

# Testing

Run backend tests using the project's configured test suite.

Example:

```bash
pytest
```

Health check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# Monitoring

Production deployments should monitor:

- API availability
- Request latency
- Error rates
- CPU usage
- Memory usage
- Disk usage
- LLM/API failures
- Vector retrieval failures
- Upload failures

The `/health` endpoint can be used by infrastructure health checks.

---

# Logging

Application logs should contain operational information such as:

```text
Request received
Request completed
Processing failed
External API failure
```

Sensitive medical information should not be written to logs.

Avoid logging:

- Full uploaded reports
- Patient names
- Medical record numbers
- Personal identifiers
- API keys
- Authentication tokens
- Complete user prompts when they contain sensitive data

---

# Development vs Production

| Area | Development | Production |
|---|---|---|
| Frontend | Vite development server | Production static build |
| Backend | Uvicorn | Uvicorn / production server |
| Configuration | `.env` | Secure environment variables |
| HTTPS | Optional | Required |
| Logs | Console | Centralized logging |
| Storage | Local | Managed storage where required |
| Scaling | Single instance | Multiple instances if required |
| Monitoring | Basic | Application and infrastructure monitoring |
| Secrets | Local environment | Secure secret management |

---

# Complete Application Flow

```text
                USER
                  │
                  ▼
           Medical PDF
           + Question
                  │
                  ▼
          ┌───────────────┐
          │ React Client  │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │   FastAPI     │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ PDF Processing│
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │     RAG       │
          │   Retrieval   │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │    FAISS      │
          └───────┬───────┘
                  │
                  ▼
          Relevant Context
                  │
                  ▼
          ┌───────────────┐
          │    LLM API    │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ Safety Check  │
          └───────┬───────┘
                  │
                  ▼
             Final Answer
                  │
                  ▼
           React Client
                  │
                  ▼
                USER
```

---

# Future Enhancements

Potential future improvements include:

- User authentication and authorization
- Persistent conversation storage
- Secure report storage
- Streaming responses
- Additional medical report formats
- Improved document extraction
- RAG citations
- Retrieval evaluation
- Automated testing
- CI/CD
- Containerized deployment
- Container orchestration
- Horizontal scaling
- Centralized logging
- Metrics and observability
- Infrastructure as Code
- Advanced privacy controls

---

# Medical Disclaimer

MedReport AI provides AI-generated informational responses based on uploaded
documents and retrieved knowledge.

The system is not intended to:

- Diagnose medical conditions
- Prescribe medication
- Replace healthcare professionals
- Make emergency medical decisions
- Provide definitive clinical conclusions
- Make autonomous clinical decisions

Users should consult a qualified healthcare professional for medical
diagnosis, treatment, and clinical decision-making.

---

# License

Add the applicable project license here.

---

# Author

**MedReport AI**

AI-powered medical report analysis and RAG application.