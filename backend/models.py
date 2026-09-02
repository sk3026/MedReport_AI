from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class LabResult:
    test_name: str
    value: Any
    unit: Optional[str] = None
    reference_low: Optional[float] = None
    reference_high: Optional[float] = None
    status: str = "unknown"
    page: Optional[int] = None
    raw_text: Optional[str] = None


@dataclass
class MedicalReport:
    report_id: str
    filename: str
    pages: int
    results: List[LabResult] = field(default_factory=list)
    raw_text: str = ""