from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.config import TEMP_REPORTS_DIR
from backend.ingestion.pdf import extract_pdf_text
from backend.ingestion.parser import parse_report
from backend.ingestion.validator import validate_report
from backend.ingestion.summary import generate_report_summary
from backend.retrieval.context import retrieve_context
from backend.retrieval.context_formatter import build_rag_context
from backend.generation.response import generate_safe_response


app = FastAPI(
    title="MedReport AI API",
    description="RAG-powered medical laboratory report explanation assistant",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sessions = {}


@app.get("/")
def root():
    return {
        "message": "MedReport AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_report(
    file: UploadFile = File(...),
    question: str = Form(...)
):

    if not file.filename:
        return {
            "success": False,
            "error": ["No file provided"]
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "error": ["Only PDF files are supported"]
        }

    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_path = TEMP_REPORTS_DIR / temp_filename

    try:

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        extracted_data = extract_pdf_text(
            str(temp_path)
        )

        medical_report = parse_report(
            extracted_data
        )

        validation = validate_report(
            medical_report
        )

        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["errors"],
                "warnings": validation["warnings"]
            }

        summary = generate_report_summary(
            medical_report
        )

        session_id = str(uuid.uuid4())

        sessions[session_id] = {
            "medical_report": medical_report,
            "filename": file.filename,
            "last_test": None,
            "history": []
        }

        retrieved_context = retrieve_context(
            question,
            medical_report,
            top_k=5
        )

        rag_context = build_rag_context(
            retrieved_context
        )

        response = generate_safe_response(
            question,
            rag_context
        )

        if retrieved_context["report_context"]:

            sessions[session_id]["last_test"] = (
                retrieved_context["report_context"][0]["test_name"]
            )

        sessions[session_id]["history"].append(
            {
                "role": "user",
                "content": question
            }
        )

        sessions[session_id]["history"].append(
            {
                "role": "assistant",
                "content": response["answer"]
            }
        )

        return {
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "summary": summary,
            "results": [
                {
                    "test_name": result.test_name,
                    "value": result.value,
                    "unit": result.unit,
                    "reference_low": result.reference_low,
                    "reference_high": result.reference_high,
                    "status": result.status,
                    "page": result.page
                }
                for result in medical_report.results
            ],
            "answer": response["answer"],
            "safe": response["safe"],
            "violations": response["violations"],
            "sources": retrieved_context["knowledge_context"]
        }

    except Exception as exc:

        return {
            "success": False,
            "error": [str(exc)]
        }

    finally:

        if temp_path.exists():
            temp_path.unlink()


@app.post("/chat")
async def chat(
    session_id: str = Form(...),
    question: str = Form(...)
):

    session = sessions.get(session_id)

    if session is None:
        return {
            "success": False,
            "error": ["Session not found"]
        }

    medical_report = session["medical_report"]

    previous_test = session.get(
        "last_test"
    )

    retrieved_context = retrieve_context(
        question,
        medical_report,
        top_k=5,
        previous_test=previous_test
    )

    rag_context = build_rag_context(
        retrieved_context
    )

    response = generate_safe_response(
        question,
        rag_context
    )

    if retrieved_context["report_context"]:

        session["last_test"] = (
            retrieved_context["report_context"][0]["test_name"]
        )

    session["history"].append(
        {
            "role": "user",
            "content": question
        }
    )

    session["history"].append(
        {
            "role": "assistant",
            "content": response["answer"]
        }
    )

    return {
        "success": True,
        "answer": response["answer"],
        "safe": response["safe"],
        "violations": response["violations"],
        "sources": retrieved_context["knowledge_context"]
    }