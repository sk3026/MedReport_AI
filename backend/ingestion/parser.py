import re

from typing import Dict, List

from backend.models import LabResult, MedicalReport


NUMBER_PATTERN = r"-?\d+(?:\.\d+)?"

RANGE_PATTERNS = [
    re.compile(
        rf"^\s*({NUMBER_PATTERN})\s*(?:-|–|—|to)\s*({NUMBER_PATTERN})\s*$",
        re.IGNORECASE,
    ),
    re.compile(
        rf"^\s*(?:<|<=|≤)\s*({NUMBER_PATTERN})\s*$",
        re.IGNORECASE,
    ),
    re.compile(
        rf"^\s*(?:>|>=|≥)\s*({NUMBER_PATTERN})\s*$",
        re.IGNORECASE,
    ),
]


def clean_lines(text: str) -> List[str]:
    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    return lines


def parse_range(text: str):
    text = text.strip()

    for pattern in RANGE_PATTERNS:
        match = pattern.match(text)

        if not match:
            continue

        if len(match.groups()) == 2:
            return float(match.group(1)), float(match.group(2))

        value = float(match.group(1))

        if text.startswith(("<", "<=", "≤")):
            return None, value

        if text.startswith((">", ">=", "≥")):
            return value, None

    return None, None


def extract_range_from_text(text: str):
    patterns = [
        re.compile(
            rf"({NUMBER_PATTERN})\s*(?:-|–|—|to)\s*({NUMBER_PATTERN})"
        ),
        re.compile(
            rf"(?:<|<=|≤)\s*({NUMBER_PATTERN})"
        ),
        re.compile(
            rf"(?:>|>=|≥)\s*({NUMBER_PATTERN})"
        ),
    ]

    for pattern in patterns:
        match = pattern.search(text)

        if not match:
            continue

        if len(match.groups()) == 2:
            return float(match.group(1)), float(match.group(2))

        value = float(match.group(1))

        if re.search(r"(?:<|<=|≤)", match.group(0)):
            return None, value

        return value, None

    return None, None


def classify_result(
    value: float,
    reference_low,
    reference_high
) -> str:

    if reference_low is not None and value < reference_low:
        return "low"

    if reference_high is not None and value > reference_high:
        return "high"

    if reference_low is not None or reference_high is not None:
        return "within_range"

    return "unknown"


def is_number(text: str) -> bool:
    try:
        float(text.strip())
        return True
    except ValueError:
        return False


def looks_like_unit(text: str) -> bool:
    text = text.strip()

    if not text:
        return False

    if is_number(text):
        return False

    if parse_range(text)[0] is not None or parse_range(text)[1] is not None:
        return False

    common_units = [
        "g/dL",
        "mg/dL",
        "mg/L",
        "mmol/L",
        "µmol/L",
        "umol/L",
        "U/L",
        "IU/L",
        "mIU/L",
        "ng/mL",
        "pg/mL",
        "cells/µL",
        "cells/uL",
        "x10^3/µL",
        "x10^3/uL",
        "%",
        "fL",
        "pg",
        "mm/hr",
    ]

    for unit in common_units:
        if unit.lower() in text.lower():
            return True

    return bool(
        re.search(
            r"(?:/[A-Za-zµμ]+|%|\b(?:mg|g|mmol|mol|ng|pg|IU|mIU|U)\b)",
            text,
            re.IGNORECASE,
        )
    )


def is_header(text: str) -> bool:
    normalized = text.lower().strip()

    headers = {
        "test",
        "test name",
        "investigation",
        "investigation name",
        "parameter",
        "parameter name",
        "result",
        "value",
        "unit",
        "reference",
        "reference range",
        "normal range",
        "biological reference interval",
        "range",
        "flag",
    }

    return normalized in headers


def parse_inline_result(line: str, page_number: int):
    range_low, range_high = extract_range_from_text(line)

    if range_low is None and range_high is None:
        return None

    range_match = re.search(
        rf"({NUMBER_PATTERN})\s*(?:-|–|—|to)\s*({NUMBER_PATTERN})",
        line,
        re.IGNORECASE,
    )

    if range_match:
        before_range = line[:range_match.start()].strip()

        value_match = re.search(
            rf"\b({NUMBER_PATTERN})\b",
            before_range
        )

        if not value_match:
            return None

        value = float(value_match.group(1))

        test_name = before_range[:value_match.start()].strip()
        unit = before_range[value_match.end():].strip()

        if not test_name:
            return None

        return LabResult(
            test_name=test_name,
            value=value,
            unit=unit or None,
            reference_low=range_low,
            reference_high=range_high,
            status=classify_result(
                value,
                range_low,
                range_high
            ),
            page=page_number,
            raw_text=line,
        )

    return None


def parse_multiline_results(
    lines: List[str],
    page_number: int
) -> List[LabResult]:

    results = []
    i = 0

    while i < len(lines):

        if is_header(lines[i]):
            i += 1
            continue

        # Format:
        # Test Name
        # Value
        # Unit
        # Reference Range

        if i + 3 < len(lines):

            test_name = lines[i]
            value_text = lines[i + 1]
            unit = lines[i + 2]
            reference_text = lines[i + 3]

            if (
                not is_header(test_name)
                and is_number(value_text)
            ):

                low, high = parse_range(reference_text)

                if low is not None or high is not None:

                    value = float(value_text)

                    results.append(
                        LabResult(
                            test_name=test_name,
                            value=value,
                            unit=unit,
                            reference_low=low,
                            reference_high=high,
                            status=classify_result(
                                value,
                                low,
                                high
                            ),
                            page=page_number,
                            raw_text=" | ".join(
                                lines[i:i + 4]
                            ),
                        )
                    )

                    i += 4
                    continue

        # Format:
        # Test Name
        # Value Unit
        # Reference Range

        if i + 2 < len(lines):

            test_name = lines[i]
            result_line = lines[i + 1]
            reference_text = lines[i + 2]

            low, high = parse_range(reference_text)

            if low is not None or high is not None:

                value_match = re.search(
                    rf"\b({NUMBER_PATTERN})\b",
                    result_line
                )

                if (
                    value_match
                    and not is_header(test_name)
                ):

                    value = float(value_match.group(1))

                    unit = (
                        result_line[
                            value_match.end():
                        ].strip()
                    )

                    results.append(
                        LabResult(
                            test_name=test_name,
                            value=value,
                            unit=unit or None,
                            reference_low=low,
                            reference_high=high,
                            status=classify_result(
                                value,
                                low,
                                high
                            ),
                            page=page_number,
                            raw_text=" | ".join(
                                lines[i:i + 3]
                            ),
                        )
                    )

                    i += 3
                    continue

        # Inline format:
        # Hemoglobin 13.5 g/dL 13-17

        inline_result = parse_inline_result(
            lines[i],
            page_number
        )

        if inline_result:
            results.append(inline_result)
            i += 1
            continue

        i += 1

    return results


def parse_report(extracted_data: Dict) -> MedicalReport:

    results = []

    for page_data in extracted_data["page_data"]:

        page_number = page_data["page"]

        lines = clean_lines(
            page_data["text"]
        )

        page_results = parse_multiline_results(
            lines,
            page_number
        )

        results.extend(page_results)

    return MedicalReport(
        report_id=f"report_{abs(hash(extracted_data['filename']))}",
        filename=extracted_data["filename"],
        pages=extracted_data["pages"],
        results=results,
        raw_text=extracted_data["full_text"],
    )