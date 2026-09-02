from backend.models import LabResult, MedicalReport


def validate_lab_result(result: LabResult) -> dict:
    errors = []

    if not result.test_name:
        errors.append("Missing test name")

    if result.value is None:
        errors.append("Missing result value")

    if (
        result.reference_low is not None
        and result.reference_high is not None
        and result.reference_low > result.reference_high
    ):
        errors.append("Invalid reference range")

    if result.status not in [
        "low",
        "high",
        "within_range",
        "unknown"
    ]:
        errors.append("Invalid status")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_report(report: MedicalReport) -> dict:
    errors = []
    warnings = []

    if not report.filename:
        errors.append("Missing filename")

    if report.pages <= 0:
        errors.append("Invalid page count")

    if not report.results:
        errors.append("No laboratory results were extracted")

    valid_results = 0

    for result in report.results:

        validation = validate_lab_result(result)

        if validation["valid"]:
            valid_results += 1
        else:
            warnings.append({
                "test": result.test_name,
                "errors": validation["errors"]
            })

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "total_results": len(report.results),
        "valid_results": valid_results
    }