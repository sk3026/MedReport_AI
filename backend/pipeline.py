from backend.ingestion.pdf import extract_pdf_text
from backend.ingestion.parser import parse_report
from backend.ingestion.validator import validate_report
from backend.ingestion.summary import generate_report_summary
from backend.retrieval.context import retrieve_context
from backend.retrieval.context_formatter import build_rag_context
from backend.generation.response import generate_safe_response


def run_medreport_pipeline(pdf_path: str, question: str):

    extracted_data = extract_pdf_text(pdf_path)

    medical_report = parse_report(extracted_data)

    validation = validate_report(medical_report)

    if not validation["valid"]:
        return {
            "success": False,
            "error": validation["errors"]
        }

    summary = generate_report_summary(
        medical_report
    )

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

    return {
        "success": True,
        "report": medical_report,
        "summary": summary,
        "answer": response["answer"],
        "safe": response["safe"],
        "violations": response["violations"],
        "sources": retrieved_context["knowledge_context"]
    }