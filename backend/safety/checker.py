import re


UNSAFE_PATTERNS = [
    r"\bI\s+diagnose\b",
    r"\byou\s+(definitely|certainly)\s+have\b",
    r"\byou\s+have\s+(diabetes|anemia|cancer|kidney disease|liver disease)\b",

    r"\bprescribe\s+\w+",
    r"\bstart\s+taking\s+\w+",
    r"\bstop\s+taking\s+\w+",

    r"\btake\s+\d+\s*(mg|g|mcg|ml)\b",
    r"\b\d+\s*(mg|g|mcg|ml)\s+(once|twice|three times)\b",

    r"\bmedication dosage\b",
    r"\bwhat medication should I take\b",
    r"\bshould I take\s+\w+",
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