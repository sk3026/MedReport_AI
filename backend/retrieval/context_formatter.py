def format_report_context(report_context, whole_report=False):
    if not report_context:
        return "No specific laboratory result was identified for this question."

    if whole_report:
        total = len(report_context)

        within_range = [
            result
            for result in report_context
            if result["status"] == "within_range"
        ]

        low = [
            result
            for result in report_context
            if result["status"] == "low"
        ]

        high = [
            result
            for result in report_context
            if result["status"] == "high"
        ]

        unknown = [
            result
            for result in report_context
            if result["status"] == "unknown"
        ]

        sections = [
            "OVERALL REPORT",
            "==============",
            f"Total parameters: {total}",
            f"Within stated reference range: {len(within_range)}",
            f"High: {len(high)}",
            f"Low: {len(low)}",
            f"Unknown: {len(unknown)}",
        ]

        if high:
            sections.append("\nHIGH RESULTS")
            sections.append("------------")

            for result in high:
                reference = "Not available"

                if (
                    result["reference_low"] is not None
                    and result["reference_high"] is not None
                ):
                    reference = (
                        f'{result["reference_low"]} - '
                        f'{result["reference_high"]}'
                    )

                sections.append(
                    f'{result["test_name"]}: '
                    f'{result["value"]} {result["unit"] or ""} '
                    f'(Reference: {reference})'
                )

        if low:
            sections.append("\nLOW RESULTS")
            sections.append("-----------")

            for result in low:
                reference = "Not available"

                if (
                    result["reference_low"] is not None
                    and result["reference_high"] is not None
                ):
                    reference = (
                        f'{result["reference_low"]} - '
                        f'{result["reference_high"]}'
                    )

                sections.append(
                    f'{result["test_name"]}: '
                    f'{result["value"]} {result["unit"] or ""} '
                    f'(Reference: {reference})'
                )

        if unknown:
            sections.append("\nUNCLASSIFIED RESULTS")
            sections.append("--------------------")

            for result in unknown:
                sections.append(
                    f'{result["test_name"]}: '
                    f'{result["value"]} {result["unit"] or ""}'
                )

        return "\n".join(sections)

    sections = []

    for result in report_context:
        reference = "Not available"

        if (
            result["reference_low"] is not None
            and result["reference_high"] is not None
        ):
            reference = (
                f'{result["reference_low"]} - '
                f'{result["reference_high"]}'
            )

        section = (
            f'Test: {result["test_name"]}\n'
            f'Result: {result["value"]} {result["unit"] or ""}\n'
            f'Reference Range: {reference}\n'
            f'Status: {result["status"]}\n'
            f'Page: {result["page"]}'
        )

        sections.append(section)

    return "\n\n".join(sections)


def format_knowledge_context(knowledge_context):
    if not knowledge_context:
        return "No relevant medical knowledge was retrieved."

    sections = []

    for i, item in enumerate(knowledge_context, start=1):
        metadata = item.get("metadata", {})

        topic = metadata.get("topic", "Unknown")
        source = metadata.get(
            "source",
            "Unknown"
        )

        section = (
            f"Source {i}\n"
            f"Topic: {topic}\n"
            f"Source: {source}\n"
            f"Relevance Score: {item['score']:.3f}\n"
            f"Content:\n{item['content']}"
        )

        sections.append(section)

    return "\n\n".join(sections)


def build_rag_context(retrieved_context):
    whole_report = retrieved_context.get(
        "whole_report",
        False
    )

    report_context = format_report_context(
        retrieved_context["report_context"],
        whole_report=whole_report
    )

    knowledge_context = format_knowledge_context(
        retrieved_context["knowledge_context"]
    )

    detected_test = retrieved_context.get(
        "detected_test"
    )

    if whole_report:
        test_section = "Question Type: Whole Report"
    elif detected_test:
        test_section = f"Detected Test: {detected_test}"
    else:
        test_section = "Detected Test: None"

    return f"""
PATIENT REPORT
==============

{test_section}

{report_context}


MEDICAL KNOWLEDGE
=================

{knowledge_context}
""".strip()