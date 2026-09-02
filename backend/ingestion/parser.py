import re
from typing import Dict, List

from backend.models import LabResult, MedicalReport


def clean_lines(text: str) -> List[str]:
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return lines


def parse_range(text: str):
    text = text.strip()

    pattern = (
        r"^\s*(-?\d+(?:\.\d+)?)\s*"
        r"(?:-|–|—|to)\s*"
        r"(-?\d+(?:\.\d+)?)\s*$"
    )

    match = re.match(pattern, text, re.IGNORECASE)

    if match:
        return float(match.group(1)), float(match.group(2))

    return None, None


def classify_result(
    value: float,
    reference_low,
    reference_high
) -> str:

    if reference_low is None or reference_high is None:
        return "unknown"

    if value < reference_low:
        return "low"

    if value > reference_high:
        return "high"

    return "within_range"


def parse_report(extracted_data: Dict) -> MedicalReport:
    results = []

    for page_data in extracted_data["page_data"]:

        page_number = page_data["page"]

        lines = clean_lines(page_data["text"])

        header_index = None

        for i, line in enumerate(lines):
            if line.lower() == "reference range":
                header_index = i
                break

        if header_index is None:
            continue

        lines = lines[header_index + 1:]

        i = 0

        while i + 3 < len(lines):

            test_name = lines[i]
            result_text = lines[i + 1]
            unit = lines[i + 2]
            reference_text = lines[i + 3]

            try:
                value = float(result_text)

            except ValueError:
                i += 1
                continue

            reference_low, reference_high = parse_range(
                reference_text
            )

            if reference_low is None:
                i += 1
                continue

            status = classify_result(
                value,
                reference_low,
                reference_high
            )

            result = LabResult(
                test_name=test_name,
                value=value,
                unit=unit,
                reference_low=reference_low,
                reference_high=reference_high,
                status=status,
                page=page_number,
                raw_text=" | ".join(lines[i:i + 5])
            )

            results.append(result)

            i += 5

    return MedicalReport(
        report_id=f"report_{abs(hash(extracted_data['filename']))}",
        filename=extracted_data["filename"],
        pages=extracted_data["pages"],
        results=results,
        raw_text=extracted_data["full_text"]
    )