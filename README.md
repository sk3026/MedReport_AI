MEDREPORT AI
Medical Report Analysis & RAG Chatbot
======================================

MedReport AI is a full-stack medical report analysis application that allows
users to upload supported medical PDF reports, ask questions about the report,
and receive context-aware answers using Retrieval-Augmented Generation (RAG).

The project combines a React frontend, FastAPI backend, PDF processing,
FAISS-based vector retrieval, SentenceTransformer embeddings, and the Groq LLM.

IMPORTANT:
This project is intended for educational and informational purposes.
It is not a replacement for a qualified medical professional or medical
diagnosis.


------------------------------------------------------------
FEATURES
------------------------------------------------------------

- Upload medical reports in PDF format.
- Validate supported medical report types.
- Extract and process text from uploaded reports.
- Generate report summaries.
- Ask natural-language questions about uploaded reports.
- Retrieve relevant medical knowledge using FAISS.
- Generate context-aware answers using the Groq LLM.
- Use SentenceTransformer locally on the backend for embeddings.
- Maintain chat sessions for follow-up questions.
- Apply a safety-checking layer before returning responses.
- React + Vite frontend.
- FastAPI REST backend.
- AWS deployment using S3, CloudFront, and EC2.
- Uvicorn managed using systemd for continuous backend operation.


------------------------------------------------------------
TECHNOLOGY STACK
------------------------------------------------------------

FRONTEND
- React
- Vite
- JavaScript
- Axios

BACKEND
- Python
- FastAPI
- Uvicorn

RAG / AI
- SentenceTransformers
- all-MiniLM-L6-v2
- FAISS
- Groq API
- LangChain text splitters

PDF / DATA PROCESSING
- PyMuPDF
- Python data-processing utilities

DEPLOYMENT
- AWS EC2
- AWS S3
- AWS CloudFront
- AWS WAF
- systemd


------------------------------------------------------------
PROJECT STRUCTURE
------------------------------------------------------------

MedReport_AI/
|
+-- backend/
|   |
|   +-- api/
|   |   +-- main.py
|   |
|   +-- ingestion/
|   |   +-- parser.py
|   |   +-- pdf.py
|   |   +-- summary.py
|   |   +-- validator.py
|   |
|   +-- knowledge/
|   |   +-- chunking.py
|   |   +-- documents.py
|   |   +-- embeddings.py
|   |   +-- vectorstore.py
|   |
|   +-- retrieval/
|   |   +-- search.py
|   |   +-- context.py
|   |   +-- context_formatter.py
|   |   +-- test_matcher.py
|   |
|   +-- generation/
|   |   +-- llm.py
|   |   +-- prompts.py
|   |   +-- response.py
|   |
|   +-- safety/
|   |   +-- checker.py
|   |
|   +-- config.py
|   +-- models.py
|   +-- pipeline.py
|
+-- data/
|   +-- knowledge_base/
|   +-- processed/
|   +-- reports/
|       +-- temp/
|
+-- vectorstore/
|   +-- medical_knowledge.index
|   +-- knowledge_documents.pkl
|
+-- frontend/
|   +-- src/
|   |   +-- App.jsx
|   +-- public/
|   +-- package.json
|   +-- dist/
|
+-- tests/
|
+-- requirements.txt
+-- .env
+-- .env.example
+-- .gitignore
+-- README.md
+-- package.json


------------------------------------------------------------
HOW THE APPLICATION WORKS
------------------------------------------------------------

The application follows this overall flow:

User
 |
 v
React Frontend
 |
 | PDF + Question
 v
FastAPI Backend
 |
 v
PDF Processing
 |
 +--> Parse
 |
 +--> Validate
 |
 +--> Generate Summary
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
 +----------------------------+
 |                            |
 v                            v
Uploaded Report Context   Retrieved Knowledge
 |                            |
 +-------------+--------------+
               |
               v
            Groq LLM
               |
               v
          Safety Checker
               |
               v
          Final Response
               |
               v
         React Frontend


------------------------------------------------------------
RAG ARCHITECTURE
------------------------------------------------------------

MedReport AI uses Retrieval-Augmented Generation (RAG).

The RAG pipeline works as follows:

1. Medical knowledge is stored in the project's knowledge base.

2. Large documents are divided into smaller chunks.

3. Each chunk is converted into a vector embedding using the
   SentenceTransformer model:

       all-MiniLM-L6-v2

4. The embeddings are stored in a FAISS vector index.

5. When the user asks a question, the question is also converted into
   an embedding using the same SentenceTransformer model.

6. FAISS performs similarity search between the question embedding and
   the stored medical knowledge embeddings.

7. The most relevant knowledge chunks are retrieved.

8. The retrieved knowledge is combined with information from the uploaded
   medical report and the user's question.

9. This context is sent to the Groq LLM.

10. The LLM generates a context-aware response.

11. The generated response passes through the safety-checking layer.

12. The final response is returned to the React frontend.


The core RAG flow is:

    User Question
         |
         v
    SentenceTransformer
         |
         v
    384-Dimensional Embedding
         |
         v
    FAISS Similarity Search
         |
         v
    Relevant Medical Context
         |
         +----------------------+
         |                      |
         v                      v
    Report Information     Retrieved Knowledge
         |                      |
         +----------+-----------+
                    |
                    v
                 Groq LLM
                    |
                    v
              Safety Checker
                    |
                    v
                Answer


------------------------------------------------------------
EMBEDDING MODEL
------------------------------------------------------------

The project uses SentenceTransformers to generate vector embeddings for
medical knowledge and user queries.

Model:

    all-MiniLM-L6-v2

Embedding dimension:

    384

The SentenceTransformer model runs locally on the backend server (EC2).

It converts text into 384-dimensional vectors, which are then used by
FAISS for similarity search.

The embedding process is:

    Text
      |
      v
    all-MiniLM-L6-v2
      |
      v
    384-dimensional embedding
      |
      v
    FAISS similarity search

Unlike the LLM, embedding generation does not require an external API call.
The model runs directly on the backend server.

The existing FAISS vectorstore is stored locally:

    vectorstore/medical_knowledge.index
    vectorstore/knowledge_documents.pkl


------------------------------------------------------------
VECTOR DATABASE
------------------------------------------------------------

The project uses FAISS for vector similarity search.

FAISS stands for Facebook AI Similarity Search.

The vectorstore contains:

    medical_knowledge.index
    knowledge_documents.pkl

The FAISS index is used to efficiently find medical knowledge that is
semantically similar to the user's question.

The configured number of retrieved results is:

    top_k = 5


------------------------------------------------------------
KNOWLEDGE PROCESSING
------------------------------------------------------------

Medical knowledge is processed before being stored in the vectorstore.

The general process is:

    Medical Documents
          |
          v
       Chunking
          |
          v
    Text Chunks
          |
          v
    SentenceTransformer
          |
          v
     Embeddings
          |
          v
        FAISS
          |
          v
    Vectorstore


Chunk configuration:

    Chunk size: 700
    Chunk overlap: 100


------------------------------------------------------------
INGESTION LAYER
------------------------------------------------------------

Location:

    backend/ingestion/

Files:

    parser.py
    pdf.py
    summary.py
    validator.py

Responsibilities:

pdf.py
    Handles PDF-related processing and text extraction.

parser.py
    Processes extracted report information into a usable structure.

validator.py
    Validates whether the uploaded document is a supported medical report.

summary.py
    Generates a summary of the uploaded report.

The ingestion flow is:

    PDF
     |
     v
    Text Extraction
     |
     v
    Parsing
     |
     v
    Validation
     |
     v
    Summary


------------------------------------------------------------
RETRIEVAL LAYER
------------------------------------------------------------

Location:

    backend/retrieval/

Files:

    search.py
    context.py
    context_formatter.py
    test_matcher.py

Responsibilities:

- Convert the user question into an embedding.
- Search the FAISS vectorstore.
- Retrieve relevant medical knowledge.
- Build the context used by the LLM.
- Format retrieved information for generation.


Retrieval flow:

    User Question
         |
         v
    Embedding
         |
         v
    FAISS
         |
         v
    Similarity Search
         |
         v
    Top 5 Relevant Chunks
         |
         v
    Retrieved Context


------------------------------------------------------------
GENERATION LAYER
------------------------------------------------------------

Location:

    backend/generation/

Files:

    llm.py
    prompts.py
    response.py

The generation layer communicates with the Groq API.

The LLM receives:

- User question
- Uploaded report information
- Retrieved medical knowledge
- Prompt instructions

The generation flow is:

    Question
       +
    Report Context
       +
    Retrieved Knowledge
       +
    Prompt
       |
       v
    Groq LLM
       |
       v
    Generated Response


------------------------------------------------------------
SAFETY LAYER
------------------------------------------------------------

Location:

    backend/safety/checker.py

The generated response is passed through a safety-checking layer before
being returned to the user.

This layer is especially important because the application deals with
medical information.

General flow:

    LLM Response
         |
         v
    Safety Checker
         |
         v
    Final Response


------------------------------------------------------------
SUPPORTED REPORT TYPES
------------------------------------------------------------

The current configuration supports:

- CBC
- Glucose
- Lipid Profile
- Liver Function
- Kidney Function
- Thyroid

Supported file type:

    .pdf


------------------------------------------------------------
BACKEND API
------------------------------------------------------------

Base URL for local development:

    http://127.0.0.1:8000

Available endpoints:

GET /
    Returns basic API information.

GET /health
    Health check endpoint used to verify that the backend is running.

POST /analyze
    Uploads a medical PDF report and processes the initial question.

POST /chat
    Continues an existing analysis session and handles follow-up questions.


------------------------------------------------------------
RUNNING THE BACKEND LOCALLY
------------------------------------------------------------

1. Create a Python virtual environment.

Windows:

    python -m venv .venv

Activate it:

    .venv\Scripts\activate


Linux / macOS:

    python -m venv .venv

Activate it:

    source .venv/bin/activate


2. Install dependencies:

    pip install -r requirements.txt


3. Create a .env file in the project root.

Example:

    GROQ_API_KEY=your_groq_api_key_here


4. Start the FastAPI server:

    uvicorn backend.api.main:app --host 0.0.0.0 --port 8000


5. Test the backend:

    http://127.0.0.1:8000/health

Expected response:

    {"status":"healthy"}


------------------------------------------------------------
RUNNING THE FRONTEND LOCALLY
------------------------------------------------------------

Go to the frontend directory:

    cd frontend


Install dependencies:

    npm install


Start the development server:

    npm run dev


The Vite development server normally runs at:

    http://localhost:5173


------------------------------------------------------------
FRONTEND ENVIRONMENT VARIABLES
------------------------------------------------------------

For local development:

    VITE_API_URL=http://127.0.0.1:8000


For production:

    VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net


IMPORTANT:

Vite embeds VITE_* variables into the frontend during the build process.

Therefore, after changing .env.production, rebuild the frontend:

    npm run build


------------------------------------------------------------
AWS DEPLOYMENT ARCHITECTURE
------------------------------------------------------------

The application is deployed on AWS using S3, CloudFront, and EC2.

Production architecture:

                         INTERNET
                             |
                             v
                     AWS CLOUDFRONT
                         HTTPS
                       /       \
                      /         \
                     v           v
                    S3          EC2
               React Frontend  FastAPI
                                  |
                                  v
                            SentenceTransformer
                                  |
                                  v
                                FAISS
                                  |
                                  v
                              Groq API


CloudFront routing:

    /              -> S3 React frontend
    /analyze       -> EC2 FastAPI
    /chat          -> EC2 FastAPI


This architecture allows the frontend and backend API to use the same
HTTPS CloudFront domain.


------------------------------------------------------------
AWS FRONTEND DEPLOYMENT
------------------------------------------------------------

The production React application is built using:

    npm run build


The generated files are located in:

    frontend/dist/


The contents of the dist directory are uploaded to the S3 frontend bucket.

The S3 bucket is kept private and is accessed through CloudFront using
Origin Access Control (OAC).

CloudFront serves the React application over HTTPS.

Default root object:

    index.html


------------------------------------------------------------
AWS BACKEND DEPLOYMENT
------------------------------------------------------------

The FastAPI application runs on an AWS EC2 instance.

Uvicorn listens on:

    0.0.0.0:8000


The backend is managed using systemd.

Service name:

    medreport.service


This allows the backend to:

- Run continuously in the background.
- Continue running after the SSH terminal is closed.
- Automatically start after an EC2 reboot.
- Automatically restart if the process stops.


Useful commands:

Check service status:

    sudo systemctl status medreport


Start service:

    sudo systemctl start medreport


Stop service:

    sudo systemctl stop medreport


Restart service:

    sudo systemctl restart medreport


View live logs:

    sudo journalctl -u medreport -f


Check port 8000:

    sudo ss -lntp | grep :8000


------------------------------------------------------------
AWS CLOUDFRONT
------------------------------------------------------------

CloudFront is used as the public HTTPS entry point.

The distribution serves:

    Frontend:
    CloudFront -> S3

    API:
    CloudFront -> EC2 -> FastAPI


CloudFront behaviors:

    Default (*)  -> S3
    /analyze     -> EC2
    /chat        -> EC2


The /analyze and /chat behaviors allow POST requests because these
endpoints receive user data.


------------------------------------------------------------
AWS WAF
------------------------------------------------------------

AWS WAF is enabled on the CloudFront distribution to provide protection
against common web attacks.

The WAF includes AWS-managed protections such as:

- Amazon IP Reputation List
- Common Rule Set
- Known Bad Inputs Rule Set

WAF requests that are blocked do not reach the EC2 backend.

Therefore, when troubleshooting a CloudFront 403 response, checking
AWS WAF sampled requests and logs can help identify the rule responsible
for blocking the request.


------------------------------------------------------------
SECURITY
------------------------------------------------------------

The project uses several security measures:

- S3 Block Public Access.
- CloudFront Origin Access Control for S3.
- HTTPS through CloudFront.
- EC2 security-group restrictions.
- AWS WAF protection.
- Environment variables for API secrets.
- Temporary storage for uploaded reports.

The Groq API key must never be committed to GitHub.

The .env file should remain private and should not be tracked by Git.


------------------------------------------------------------
ENVIRONMENT VARIABLES
------------------------------------------------------------

Required environment variable:

    GROQ_API_KEY


Example:

    GROQ_API_KEY=your_groq_api_key_here


Never place the real API key directly in source code.

Never commit the real .env file to GitHub.


------------------------------------------------------------
TESTING
------------------------------------------------------------

Backend health check:

    curl http://127.0.0.1:8000/health


Test the deployed API endpoint:

    curl -i -X POST https://dwtdehq0kif0o.cloudfront.net/analyze


A POST request without the required file and question should return a
validation error from FastAPI.

For example:

    422 Unprocessable Content

This confirms that the request successfully reached the FastAPI backend.


------------------------------------------------------------
TROUBLESHOOTING
------------------------------------------------------------

1. BACKEND IS NOT RESPONDING

Check:

    sudo systemctl status medreport

View logs:

    sudo journalctl -u medreport -f

Check port:

    sudo ss -lntp | grep :8000


2. FRONTEND SHOWS AN API OR NETWORK ERROR

Check the production API URL:

    VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net

Rebuild:

    npm run build

Upload the new dist contents to S3.

Then invalidate the CloudFront cache if required.


3. CLOUDFRONT RETURNS 504

Check:

- systemd/Uvicorn status.
- EC2 port 8000.
- EC2 security-group rules.
- CloudFront origin configuration.
- CloudFront behavior configuration.
- EC2 public DNS/address.


4. CLOUDFRONT RETURNS 403

If FastAPI logs show no corresponding request, the request may have been
blocked by CloudFront or AWS WAF before reaching EC2.

Check:

- CloudFront behavior.
- Allowed HTTP methods.
- AWS WAF sampled requests.
- AWS WAF rules and actions.
- CloudFront cache/invalidation state.


5. PDF UPLOAD IS BLOCKED

If an empty POST reaches FastAPI but a multipart PDF upload returns a
CloudFront 403, investigate AWS WAF rules that inspect request bodies.

Use WAF sampled requests/logging to identify the exact rule responsible
before changing or disabling a security rule.


6. HUGGING FACE WARNING

SentenceTransformers may display a warning about unauthenticated requests
to the Hugging Face Hub.

A Hugging Face token is not required for the application when the required
model files are already available or can be downloaded.

The SentenceTransformer model itself runs locally on the backend after
being loaded.


------------------------------------------------------------
IMPORTANT DEPLOYMENT NOTE
------------------------------------------------------------

The production frontend must be rebuilt whenever VITE_API_URL changes.

For example:

    VITE_API_URL=https://dwtdehq0kif0o.cloudfront.net

Then:

    npm run build


After building, upload the updated contents of:

    frontend/dist/

to S3.

If CloudFront continues serving an older version, create an invalidation:

    /*


------------------------------------------------------------
PROJECT ARCHITECTURE SUMMARY
------------------------------------------------------------

Frontend:

    React + Vite
          |
          v
    AWS S3 + CloudFront


Backend:

    AWS EC2
       |
       v
    Uvicorn
       |
       v
    FastAPI


RAG:

    User Question
         |
         v
    SentenceTransformer
         |
         v
    Embedding
         |
         v
    FAISS
         |
         v
    Relevant Knowledge
         |
         v
    Groq LLM
         |
         v
    Safety Checker
         |
         v
    Final Answer


Complete application:

    React
      |
      v
    CloudFront
      |
      +----------------------+
      |                      |
      v                      v
     S3                    EC2
  Frontend              FastAPI
                           |
                           +--> PDF Processing
                           |
                           +--> SentenceTransformer
                           |
                           +--> FAISS
                           |
                           +--> Groq
                           |
                           +--> Safety Checker
                           |
                           v
                         Answer


------------------------------------------------------------
FUTURE IMPROVEMENTS
------------------------------------------------------------

Possible future improvements include:

- User authentication and authorization.
- Persistent database for chat sessions.
- Secure object storage for uploaded reports.
- Streaming LLM responses.
- More advanced medical-document parsing.
- Support for additional medical report formats.
- RAG source/citation display.
- Automated RAG evaluation.
- Improved monitoring and logging.
- CI/CD deployment pipeline.
- Infrastructure as code using Terraform or AWS CDK.
- Stronger privacy and compliance controls.


------------------------------------------------------------
MEDICAL SAFETY NOTICE
------------------------------------------------------------

MedReport AI is an AI-assisted informational application.

The generated information should not be considered a medical diagnosis,
prescription, or substitute for professional medical advice.

Users should consult a qualified healthcare professional for diagnosis,
treatment decisions, or interpretation of serious medical conditions.


------------------------------------------------------------
AUTHOR
------------------------------------------------------------

MedReport AI
Full-Stack Medical Report Analysis and RAG Chatbot


------------------------------------------------------------
LICENSE
------------------------------------------------------------

Add the project's license information here if applicable.