from backend.ingestion.pdf import extract_pdf_text
from backend.ingestion.parser import parse_report
from backend.ingestion.validator import validate_report
from backend.ingestion.summary import generate_report_statistics


PDF_PATH = "data/reports/blood_report.pdf"


def get_medical_report():
    extracted_data = extract_pdf_text(PDF_PATH)
    return parse_report(extracted_data)


def test_pdf_extraction():
    extracted_data = extract_pdf_text(PDF_PATH)

    assert extracted_data["pages"] > 0
    assert extracted_data["full_text"]


def test_report_parsing():
    medical_report = get_medical_report()

    assert len(medical_report.results) > 0


def test_expected_number_of_results():
    medical_report = get_medical_report()

    assert len(medical_report.results) == 18


def test_report_validation():
    medical_report = get_medical_report()
    validation = validate_report(medical_report)

    assert validation["valid"] is True
    assert validation["total_results"] == 18


def test_fasting_glucose():
    medical_report = get_medical_report()

    glucose = next(
        result
        for result in medical_report.results
        if result.test_name == "Fasting Glucose"
    )

    assert glucose.value == 92.0
    assert glucose.reference_low == 70.0
    assert glucose.reference_high == 99.0
    assert glucose.status == "within_range"


def test_report_statistics():
    medical_report = get_medical_report()
    stats = generate_report_statistics(medical_report)

    assert stats["total_parameters"] == 18
    assert (
        stats["within_range"]
        + stats["low"]
        + stats["high"]
        + stats["unknown"]
        == 18
    )