MEDREPORT AI Medical Report Analysis & RAG Chatbot
=====================================

MedReport AI is a full-stack medical report analysis application that
allows users to upload supported medical PDF reports, ask questions
about the report, and receive context-aware answers using
Retrieval-Augmented Generation (RAG).

The project combines a React frontend, FastAPI backend, PDF processing,
FAISS-based vector retrieval, SentenceTransformer embeddings, and the
Groq LLM.

IMPORTANT: This project is intended for educational and informational
purposes. It is not a replacement for a qualified medical professional
or medical diagnosis.

FEATURES

-   Upload medical reports in PDF format.
-   Validate supported report types.
-   Extract and process text from uploaded reports.
-   Generate report summaries.
-   Ask natural-language questions about uploaded reports.
-   Retrieve relevant medical knowledge using FAISS.
-   Generate answers using a Groq-hosted LLM.
-   Use local SentenceTransformer embeddings.
-   Maintain chat sessions for follow-up questions.
-   Apply a safety-checking layer before returning responses.
-   React + Vite frontend.
-   FastAPI REST backend.
-   Production deployment using AWS S3, CloudFront, and EC2.

TECHNOLOGY STACK

Frontend: - React - Vite - JavaScript - Axios

Backend: - Python - FastAPI - Uvicorn

RAG / AI: - SentenceTransformers - all-MiniLM-L6-v2 - FAISS - Groq LLM -
LangChain text splitters

PDF / Data Processing: - PyMuPDF - Python data-processing utilities

Deployment: - AWS EC2 - AWS S3 - AWS CloudFront - AWS WAF - systemd

PROJECT STRUCTURE

MedReport_AI/ | +– backend/ | | | +– api/ | | +– main.py | | | +–
ingestion/ | | +– parser.py | | +– pdf.py | | +– summary.py | | +–
validator.py | | | +– knowledge/ | | +– chunking.py | | +– documents.py
| | +– embeddings.py | | +– vectorstore.py | | | +– retrieval/ | | +–
search.py | | +– context.py | | +– context_formatter.py | | +–
test_matcher.py | | | +– generation/ | | +– llm.py | | +– prompts.py | |
+– response.py | | | +– safety/ | | +– checker.py | | | +– config.py |
+– models.py | +– pipeline.py | +– data/ | +– knowledge_base/ | +–
processed/ | +– reports/ | +– temp/ | +– vectorstore/ | +–
medical_knowledge.index | +– knowledge_documents.pkl | +– frontend/ | +–
src/ | | +– App.jsx | +– public/ | +– package.json | +– dist/ | +–
tests/ | +– requirements.txt +– .env +– .env.example +– .gitignore +–
README.md +– package.json

HOW THE APPLICATION WORKS

The application follows this high-level flow:

    User
      |
      v
    React Frontend
      |
      | PDF + Question
      v
    FastAPI /analyze
      |
      v
    PDF Processing
      |
      +--> Parse
      |
      +--> Validate
      |
      +--> Summarize
      |
      v
    Question Embedding
      |
      v
    FAISS Similarity Search
      |
      v
    Relevant Medical Knowledge
      |
      +----------------------+
      |                      |
      v                      v
    Report Context       Retrieved Context
      |                      |
      +----------+-----------+
                 |
                 v
              Groq LLM
                 |
                 v
            Safety Check
                 |
                 v
             Final Answer
                 |
                 v
           React Frontend

RAG PIPELINE

1.  Medical knowledge is stored in the project’s knowledge base.

2.  Large documents are divided into smaller chunks.

3.  Chunks are converted into vector embeddings using:

        all-MiniLM-L6-v2

4.  The embeddings are stored in a FAISS index.

5.  When a user asks a question, the question is converted into an
    embedding.

6.  FAISS performs similarity search against the stored medical
    knowledge.

7.  The most relevant chunks are retrieved.

8.  The retrieved context is combined with information from the uploaded
    medical report and the user’s question.

9.  The combined context is sent to the Groq LLM.

10. The generated response is passed through the safety layer.

11. The final response is returned to the frontend.

EMBEDDING MODEL

Model:

    all-MiniLM-L6-v2

Embedding dimension:

    384

Embeddings are normalized before being used for similarity search.

The existing FAISS vectorstore is stored locally:

    vectorstore/medical_knowledge.index
    vectorstore/knowledge_documents.pkl

SUPPORTED REPORT TYPES

The current configuration supports:

-   CBC
-   Glucose
-   Lipid Profile
-   Liver Function
-   Kidney Function
-   Thyroid

Supported file type:

    .pdf

BACKEND API

Base URL (local):

    http://127.0.0.1:8000

Endpoints:

GET / Basic API information.

GET /health Health check endpoint.

POST /analyze Upload a PDF report and ask an initial question.

POST /chat Continue a conversation using an existing analysis session.

RUNNING THE BACKEND LOCALLY

1.  Create and activate a Python virtual environment.

Windows:

    python -m venv .venv
    .venv\Scripts\activate

Linux / macOS:

    python -m venv .venv
    source .venv/bin/activate

2.  Install dependencies:

    pip install -r requirements.txt

3.  Create a .env file in the project root.

Example:

    GROQ_API_KEY=your_groq_api_key_here

4.  Start FastAPI:

    uvicorn backend.api.main:app –host 0.0.0.0 –port 8000

5.  Open:

    http://127.0.0.1:8000/health

Expected response:

    {"status":"healthy"}

RUNNING THE FRONTEND LOCALLY

Go to the frontend directory:

    cd frontend

Install dependencies:

    npm install

For local development:

    npm run dev

The Vite development server normally runs at:

    http://localhost:5173

FRONTEND ENVIRONMENT VARIABLES

For local development, the frontend can use:

    VITE_API_URL=http://127.0.0.1:8000

For production deployment through CloudFront:

    VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net

IMPORTANT:

Vite embeds VITE_* variables into the frontend during the build process.
Therefore, after changing .env.production, rebuild the frontend:

    npm run build

AWS DEPLOYMENT

The production architecture is:

                     Internet
                         |
                         v
                 AWS CloudFront
                    HTTPS
                  /       \
                 /         \
                v           v
              S3          EC2
           React App    FastAPI
                           |
                           v
                         FAISS
                           |
                           v
                         Groq

CloudFront routes:

    /              -> S3 frontend
    /analyze       -> EC2 FastAPI
    /chat          -> EC2 FastAPI

The frontend and backend therefore use the same HTTPS CloudFront domain.

AWS FRONTEND DEPLOYMENT

The React production build is generated with:

    npm run build

The contents of:

    frontend/dist/

are uploaded to the S3 frontend bucket.

CloudFront serves the S3 content over HTTPS.

The CloudFront distribution uses:

    index.html

as the default root object.

AWS BACKEND DEPLOYMENT

The FastAPI application runs on an EC2 instance using Uvicorn.

The backend listens on:

    0.0.0.0:8000

Uvicorn is managed by systemd using:

    medreport.service

This allows the backend to:

-   Run in the background.
-   Continue running after an SSH session closes.
-   Automatically start after an EC2 reboot.
-   Restart automatically if the process fails.

Useful commands:

Check status:

    sudo systemctl status medreport

Start:

    sudo systemctl start medreport

Stop:

    sudo systemctl stop medreport

Restart:

    sudo systemctl restart medreport

View logs:

    sudo journalctl -u medreport -f

AWS SECURITY

The production setup uses:

-   S3 Block Public Access for the frontend bucket.
-   CloudFront Origin Access Control (OAC) for S3.
-   CloudFront HTTPS for the public application.
-   EC2 security-group restrictions for backend access.
-   AWS WAF protection on CloudFront.

Do not commit secrets to Git.

The .env file should remain local/server-side and should never contain
hard-coded secrets in source code.

ENVIRONMENT VARIABLES

Required:

    GROQ_API_KEY

Example .env:

    GROQ_API_KEY=your_groq_api_key_here

Never commit the real API key to GitHub.

TESTING

Backend health check:

    curl http://127.0.0.1:8000/health

Test the deployed API endpoint:

    curl -i -X POST https://dwtdehq0kif0o.cloudfront.net/analyze

A POST request without the required fields should return a validation
error, which confirms that the request reached FastAPI.

TROUBLESHOOTING

1.  Backend is not responding

Check:

    sudo systemctl status medreport

Then:

    sudo journalctl -u medreport -f

Check port:

    sudo ss -lntp | grep :8000

2.  Frontend shows an API/network error

Check the production API URL:

    VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net

Then rebuild:

    npm run build

Upload the new dist contents to S3 and invalidate the CloudFront cache.

3.  CloudFront returns 504

Check:

-   Uvicorn/systemd status.
-   EC2 port 8000.
-   EC2 security-group rules.
-   CloudFront origin configuration.
-   CloudFront behavior for /analyze and /chat.

4.  CloudFront returns 403 for PDF upload

Check AWS WAF and its sampled requests/logs.

A request blocked by WAF does not reach FastAPI, so the absence of a
corresponding Uvicorn request is an important diagnostic signal.

5.  Hugging Face authentication warning

SentenceTransformers may display a warning about unauthenticated
requests to the Hugging Face Hub.

A Hugging Face token is not required for the local model to function
when the required model files are already available/downloadable.

PRODUCTION NOTES

For a real medical production system, additional security and compliance
controls would be required.

Recommended improvements include:

-   HTTPS everywhere.
-   Strong authentication and authorization.
-   Encryption at rest and in transit.
-   Secure secret management.
-   Strict file-size and file-type validation.
-   Malware scanning for uploaded files.
-   Secure storage and controlled retention of medical reports.
-   Audit logging.
-   Rate limiting.
-   Monitoring and alerting.
-   Appropriate privacy and regulatory compliance.
-   Avoid storing personally identifiable medical information
    unnecessarily.

This project should not be treated as a clinically validated diagnostic
system.

FUTURE IMPROVEMENTS

Possible improvements:

-   Persistent database for chat sessions.
-   Object storage for reports with secure access controls.
-   Streaming LLM responses.
-   Better medical-document parsing.
-   More report formats.
-   Authentication and user accounts.
-   Automated evaluation of RAG retrieval quality.
-   RAG citation/source display.
-   Improved observability and monitoring.
-   CI/CD deployment pipeline.
-   Infrastructure-as-code using Terraform or AWS CDK.

AUTHOR

MedReport AI Full-stack RAG-based Medical Report Analysis Application

LICENSE

Add the project’s license here if applicable.
