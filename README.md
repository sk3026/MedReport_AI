# MedReport AI

**AI-Powered Medical Report Analysis using RAG**

MedReport AI is a full-stack application that allows users to upload medical
PDF reports, ask questions about them, and receive context-aware answers.

The application uses **Retrieval-Augmented Generation (RAG)** to combine
information from the uploaded report with relevant medical knowledge before
generating an answer.

> **Note:** This project is for educational and informational purposes only.
> It is not a replacement for professional medical advice or diagnosis.

---

## Features

- Upload medical reports in PDF format
- Extract text from medical reports
- Validate supported report types
- Generate report summaries
- Ask questions about uploaded reports
- Retrieve relevant medical knowledge using FAISS
- Generate answers using Groq LLM
- Local text embeddings using SentenceTransformer
- Follow-up chat using session-based conversations
- Safety checking before returning responses
- React frontend
- FastAPI backend
- AWS deployment
- Automatic backend restart using systemd

---

## Technology

### Frontend

- React
- Vite
- JavaScript
- Axios

### Backend

- Python
- FastAPI
- Uvicorn

### RAG

- SentenceTransformers
- `all-MiniLM-L6-v2`
- FAISS
- LangChain text splitters
- Groq API

### PDF Processing

- PyMuPDF

### AWS

- Amazon S3
- Amazon CloudFront
- Amazon EC2
- AWS WAF
- systemd

---

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
├── .env
├── .env.example
├── .gitignore
├── README.md
└── package.json
```

---

## How It Works

The complete application flow is:

```text
                         USER
                           │
                           ▼
                  ┌────────────────┐
                  │ React Frontend │
                  └───────┬────────┘
                          │
                    PDF + Question
                          │
                          ▼
                  ┌────────────────┐
                  │ FastAPI Server │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ PDF Processing │
                  └───────┬────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
            Parse      Validate    Summary
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
                    User Question
                          │
                          ▼
              ┌─────────────────────┐
              │ SentenceTransformer │
              │ all-MiniLM-L6-v2    │
              └──────────┬──────────┘
                         │
                    384-D Vector
                         │
                         ▼
                  ┌─────────────┐
                  │    FAISS    │
                  └──────┬──────┘
                         │
                  Relevant Knowledge
                         │
                         ▼
              ┌─────────────────────┐
              │  Context Building   │
              └──────────┬──────────┘
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       Report Context       Medical Knowledge
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Groq LLM  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Safety Check│
                  └──────┬──────┘
                         │
                         ▼
                    Final Answer
                         │
                         ▼
                  React Frontend
                         │
                         ▼
                        USER
```

---

## RAG Pipeline

RAG stands for **Retrieval-Augmented Generation**.

Instead of sending only the user's question to the LLM, the application
first retrieves relevant medical information and provides it as context.

### Knowledge Preparation

```text
Medical Documents
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
  384-D Vectors
       │
       ▼
      FAISS
       │
       ▼
  Vectorstore
```

### User Question

```text
User Question
      │
      ▼
SentenceTransformer
      │
      ▼
Question Vector
      │
      ▼
FAISS Search
      │
      ▼
Top 5 Relevant Chunks
      │
      ▼
Retrieved Context
```

### Answer Generation

```text
Uploaded Report
       +
Retrieved Knowledge
       +
User Question
       │
       ▼
    Groq LLM
       │
       ▼
  Safety Check
       │
       ▼
 Final Answer
```

---

## Embeddings

The project uses the following SentenceTransformer model:

```text
all-MiniLM-L6-v2
```

The model generates:

```text
384-dimensional embeddings
```

The SentenceTransformer model runs **locally on the backend EC2 server**.

This means embedding generation does not require a separate external
embedding API.

The process is:

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

## Vector Database

The project uses **FAISS** for vector similarity search.

The vectorstore contains:

```text
vectorstore/
├── medical_knowledge.index
└── knowledge_documents.pkl
```

When a user asks a question, the question is converted into an embedding
and compared with the stored embeddings.

The application retrieves the most relevant knowledge chunks.

Current configuration:

```text
Top K = 5
```

---

## Medical Knowledge

The knowledge processing pipeline is:

```text
Medical Documents
       │
       ▼
     Chunk
       │
       ▼
    Embed
       │
       ▼
    Store
       │
       ▼
     FAISS
```

Current chunk configuration:

```text
Chunk Size    = 700
Chunk Overlap = 100
```

---

## Report Processing

Uploaded reports are processed through the ingestion layer.

```text
PDF
 │
 ▼
Extract Text
 │
 ▼
Parse
 │
 ▼
Validate
 │
 ▼
Generate Summary
```

The ingestion code is located in:

```text
backend/ingestion/
```

### Main Files

| File | Purpose |
|---|---|
| `pdf.py` | PDF processing and text extraction |
| `parser.py` | Parse report information |
| `validator.py` | Validate the report |
| `summary.py` | Generate report summary |

---

## Retrieval

The retrieval code is located in:

```text
backend/retrieval/
```

Main responsibilities:

- Convert questions into embeddings
- Search the FAISS index
- Find relevant medical knowledge
- Prepare retrieved context
- Format context for the LLM

Main files:

```text
search.py
context.py
context_formatter.py
test_matcher.py
```

---

## Answer Generation

The generation code is located in:

```text
backend/generation/
```

Main files:

```text
llm.py
prompts.py
response.py
```

The LLM receives:

```text
User Question
      +
Medical Report Context
      +
Retrieved Knowledge
      +
Prompt Instructions
```

The combined information is sent to the Groq API.

---

## Safety

The safety layer is located in:

```text
backend/safety/checker.py
```

The generated response passes through the safety checker before being
returned to the user.

```text
Groq Response
      │
      ▼
Safety Check
      │
      ▼
Final Response
```

---

## Supported Reports

Currently supported report types include:

```text
CBC
Glucose
Lipid Profile
Liver Function
Kidney Function
Thyroid
```

Supported file format:

```text
PDF
```

---

# API

## Base URL

### Local

```text
http://127.0.0.1:8000
```

### Production

```text
https://dwtdehq0kif0o.cloudfront.net
```

---

## Endpoints

### GET /

Basic API information.

```text
GET /
```

### GET /health

Checks whether the backend is running.

```text
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### POST /analyze

Uploads a medical report and asks the initial question.

```text
POST /analyze
```

The request contains:

```text
file
question
```

### POST /chat

Continues an existing chat session.

```text
POST /chat
```

---

# Local Setup

## 1. Clone the Project

```bash
git clone https://github.com/sk3026/MedReport_AI.git
cd MedReport_AI
```

---

## 2. Create Python Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
.env
```

Add:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit the real `.env` file to GitHub.

---

# Run Backend

Start FastAPI with:

```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

Test:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# Run Frontend

Move into the frontend directory:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

---

# Frontend Configuration

For local development:

```text
VITE_API_URL=http://127.0.0.1:8000
```

For production:

```text
VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net
```

After changing `VITE_API_URL`, rebuild the frontend:

```bash
npm run build
```

---

# AWS Deployment

The production architecture is:

```text
                         INTERNET
                             │
                             ▼
                      ┌─────────────┐
                      │ CloudFront  │
                      │   HTTPS     │
                      └──────┬──────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
          ┌─────────────┐         ┌─────────────┐
          │     S3      │         │     EC2     │
          │   Frontend  │         │   Backend   │
          └─────────────┘         └──────┬──────┘
                                         │
                              ┌──────────┼──────────┐
                              │          │          │
                              ▼          ▼          ▼
                       SentenceModel  FAISS      Groq
```

---

## AWS Frontend

The React application is built using:

```bash
npm run build
```

The generated files are stored in:

```text
frontend/dist/
```

The contents of `dist` are uploaded to an S3 bucket.

CloudFront serves the React application over HTTPS.

The default root object is:

```text
index.html
```

---

## AWS Backend

The FastAPI backend runs on an EC2 instance.

Uvicorn listens on:

```text
0.0.0.0:8000
```

The backend is managed using:

```text
systemd
```

Service:

```text
medreport.service
```

This allows the backend to:

- Run in the background
- Continue running after SSH is closed
- Start automatically after EC2 reboot
- Restart automatically if the process fails

---

# Systemd Commands

Check backend:

```bash
sudo systemctl status medreport
```

Start:

```bash
sudo systemctl start medreport
```

Stop:

```bash
sudo systemctl stop medreport
```

Restart:

```bash
sudo systemctl restart medreport
```

View live logs:

```bash
sudo journalctl -u medreport -f
```

Check port:

```bash
sudo ss -lntp | grep :8000
```

---

# CloudFront Routing

CloudFront routes requests based on the path.

```text
/ 
 │
 └──> S3
      React Frontend


/analyze
 │
 └──> EC2
      FastAPI


/chat
 │
 └──> EC2
      FastAPI
```

This allows the frontend and backend to use the same HTTPS domain.

---

# AWS Security

The deployment uses:

- S3 Block Public Access
- CloudFront Origin Access Control
- HTTPS through CloudFront
- EC2 security groups
- AWS WAF
- Environment variables for secrets
- Temporary report storage

The Groq API key must never be placed directly in source code.

Never commit:

```text
.env
```

to GitHub.

---

# Environment Variables

The backend requires:

```text
GROQ_API_KEY
```

Example:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The frontend uses:

```text
VITE_API_URL
```

Local:

```text
VITE_API_URL=http://127.0.0.1:8000
```

Production:

```text
VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net
```

---

# Testing

## Backend Health

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

## API Test

```bash
curl -i -X POST https://dwtdehq0kif0o.cloudfront.net/analyze
```

Without the required fields, FastAPI should return a validation error.

Example:

```text
422 Unprocessable Content
```

This confirms that the request reached the FastAPI backend.

---

# Troubleshooting

## Backend Stops

Check:

```bash
sudo systemctl status medreport
```

View logs:

```bash
sudo journalctl -u medreport -f
```

---

## Port 8000 Not Listening

Run:

```bash
sudo ss -lntp | grep :8000
```

If nothing appears:

```bash
sudo systemctl restart medreport
```

---

## CloudFront 504

Check:

```text
EC2
 ↓
Uvicorn
 ↓
FastAPI :8000
```

Also check:

- EC2 security group
- CloudFront origin
- CloudFront behavior
- EC2 public DNS
- Backend service status

---

## CloudFront 403

If the request does not appear in FastAPI logs, the request may be blocked
before reaching EC2.

Check:

- CloudFront behavior
- Allowed HTTP methods
- AWS WAF
- WAF sampled requests
- WAF rules
- CloudFront cache

---

## Frontend API Error

Check:

```text
VITE_API_URL
```

For production it should be:

```text
https://dwtdehq0kif0o.cloudfront.net
```

After changing it:

```bash
npm run build
```

Upload the new `dist` contents to S3.

If necessary, invalidate CloudFront:

```text
/*
```

---

# Deployment Flow

The overall production flow is:

```text
Developer
    │
    ▼
GitHub
    │
    ├───────────────┐
    │               │
    ▼               ▼
Frontend          Backend
    │               │
    ▼               ▼
    S3              EC2
    │               │
    └───────┬───────┘
            │
            ▼
        CloudFront
            │
            ▼
          Users
```

---

# Complete AI Flow

```text
User uploads PDF
       │
       ▼
React Frontend
       │
       ▼
CloudFront
       │
       ▼
FastAPI
       │
       ▼
PDF Processing
       │
       ├── Parse
       ├── Validate
       └── Summary
       │
       ▼
User Question
       │
       ▼
SentenceTransformer
       │
       ▼
Question Embedding
       │
       ▼
FAISS
       │
       ▼
Relevant Medical Knowledge
       │
       ├───────────────┐
       │               │
       ▼               ▼
Report Context    Retrieved Context
       │               │
       └───────┬───────┘
               │
               ▼
            Groq LLM
               │
               ▼
          Safety Check
               │
               ▼
          Final Answer
               │
               ▼
         React Frontend
               │
               ▼
              User
```

---

# Important Design Decisions

## Why FAISS?

FAISS provides efficient similarity search over vector embeddings and is
suitable for the project's local medical knowledge retrieval.

## Why SentenceTransformer?

SentenceTransformer converts text into semantic vector representations.

The same model is used for:

```text
Medical Knowledge → Embeddings
User Question     → Embedding
```

This allows FAISS to compare the question with stored knowledge.

## Why Groq?

Groq provides the LLM used for generating the final natural-language answer.

## Why RAG?

RAG allows the LLM to use retrieved medical knowledge rather than relying
only on its pretrained knowledge.

The basic idea is:

```text
Retrieve relevant information
            +
Generate answer using that information
            =
RAG
```

---

# Security and Privacy

This application handles medical information, so production systems require
strong security and privacy controls.

Recommended improvements include:

- User authentication
- Authorization
- Encryption
- Secure secret management
- Secure report storage
- File-size limits
- File-type validation
- Malware scanning
- Access control
- Audit logging
- Rate limiting
- Monitoring
- Data retention policies
- Appropriate privacy and regulatory compliance

Do not upload real patient information to public repositories.

---

# Future Improvements

Possible future improvements:

- User authentication
- Persistent database
- Persistent chat history
- Secure report storage
- Streaming responses
- More medical report types
- Better PDF parsing
- RAG source citations
- RAG evaluation
- Automated testing
- CI/CD pipeline
- Terraform or AWS CDK
- Monitoring and alerts
- Improved privacy controls

---

# Medical Disclaimer

MedReport AI is an AI-assisted informational application.

The results generated by the system should not be considered a medical
diagnosis, prescription, or substitute for professional medical advice.

Users should consult a qualified healthcare professional for diagnosis,
treatment decisions, or interpretation of serious medical conditions.

---

# Author

**MedReport AI**

Full-Stack Medical Report Analysis and RAG Application