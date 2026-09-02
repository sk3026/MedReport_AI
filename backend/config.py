from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
TEMP_REPORTS_DIR = REPORTS_DIR / "temp"
KNOWLEDGE_DIR = DATA_DIR / "knowledge_base"
PROCESSED_DIR = DATA_DIR / "processed"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"


REPORTS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)


CONFIG = {
    "project_name": "MedReport AI",
    "chunk_size": 700,
    "chunk_overlap": 100,
    "top_k": 5,
    "supported_report_types": [
        "CBC",
        "Glucose",
        "Lipid Profile",
        "Liver Function",
        "Kidney Function",
        "Thyroid",
    ],
    "supported_file_types": [".pdf"],
}