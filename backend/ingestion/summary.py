from backend.models import MedicalReport


def generate_report_statistics(report: MedicalReport) -> dict:

    total = len(report.results)

    low = [
        r for r in report.results
        if r.status == "low"
    ]

    high = [
        r for r in report.results
        if r.status == "high"
    ]

    within_range = [
        r for r in report.results
        if r.status == "within_range"
    ]

    unknown = [
        r for r in report.results
        if r.status == "unknown"
    ]

    return {
        "total_parameters": total,
        "within_range": len(within_range),
        "low": len(low),
        "high": len(high),
        "unknown": len(unknown),
        "outside_range": len(low) + len(high)
    }


def generate_report_summary(report: MedicalReport) -> str:

    stats = generate_report_statistics(report)

    summary = []

    summary.append(
        f"The report contains "
        f"{stats['total_parameters']} "
        f"identified laboratory parameters."
    )

    summary.append(
        f"{stats['within_range']} results are within "
        f"the reference ranges stated in the report."
    )

    if stats["outside_range"] > 0:
        summary.append(
            f"{stats['outside_range']} results are outside "
            f"the stated reference ranges."
        )

    if stats["unknown"] > 0:
        summary.append(
            f"{stats['unknown']} results could not be classified "
            f"because a valid reference range was unavailable."
        )

    return " ".join(summary)