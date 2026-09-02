import re


UNSAFE_PATTERNS = [
    r"\bdiagnos(e|is|ed|ing)\b",
    r"\bprescrib(e|e me|ed|ing)\b",
    r"\bprescription\b",
    r"\btake\s+\d+\s*(mg|g|mcg|ml)\b",
    r"\b(start|stop)\s+(taking\s+)?\w+\b",
    r"\bmedication dosage\b",
    r"\bdosage\b",
    r"\bshould i take\b",
    r"\bwhat medication should i take\b",
]


def check_response(text: str) -> dict:

    violations = []

    text_lower = text.lower()

    for pattern in UNSAFE_PATTERNS:

        if re.search(pattern, text_lower):
            violations.append(pattern)

    return {
        "safe": len(violations) == 0,
        "violations": violations,
    }