import numpy as np

from backend.models import MedicalReport
from backend.retrieval.search import search_knowledge
from backend.knowledge.embeddings import embedding_model


WHOLE_REPORT_KEYWORDS = [
    "my report",
    "whole report",
    "entire report",
    "overall report",
    "all my results",
    "all results",
    "my results",
    "report good",
    "report okay",
    "report normal",
    "anything abnormal",
    "any abnormal",
    "which results are abnormal",
    "which tests are abnormal",
]


def is_whole_report_question(query: str) -> bool:
    query_lower = query.lower()

    return any(
        keyword in query_lower
        for keyword in WHOLE_REPORT_KEYWORDS
    )


def find_matching_test(query: str, medical_report: MedicalReport):
    if not medical_report.results:
        return None

    query_lower = query.lower()

    # Exact test-name match
    for result in medical_report.results:
        if result.test_name.lower() in query_lower:
            return result.test_name

    # Common aliases
    aliases = {
        "blood sugar": "Fasting Glucose",
        "sugar": "Fasting Glucose",
        "glucose": "Fasting Glucose",
        "fasting sugar": "Fasting Glucose",

        "a1c": "HbA1c",
        "hba1c": "HbA1c",
        "glycated hemoglobin": "HbA1c",

        "kidney function": "Creatinine",
        "creatinine": "Creatinine",

        "hemoglobin": "Hemoglobin",
        "hb": "Hemoglobin",

        "white blood cells": "White Blood Cell Count",
        "white blood cell": "White Blood Cell Count",
        "wbc": "White Blood Cell Count",

        "ldl": "LDL Cholesterol",
        "bad cholesterol": "LDL Cholesterol",

        "hdl": "HDL Cholesterol",
        "good cholesterol": "HDL Cholesterol",
    }

    for alias, test_name in aliases.items():
        if alias in query_lower:
            for result in medical_report.results:
                if result.test_name.lower() == test_name.lower():
                    return result.test_name

    # Semantic matching as fallback
    test_names = [
        result.test_name
        for result in medical_report.results
    ]

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )[0]

    test_embeddings = embedding_model.encode(
        test_names,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    similarities = np.dot(
        test_embeddings,
        query_embedding
    )

    best_index = int(np.argmax(similarities))
    best_score = float(similarities[best_index])

    if best_score < 0.35:
        return None

    return test_names[best_index]


def retrieve_report_context(
    query,
    medical_report,
    previous_test=None
):
    # Whole-report question
    if is_whole_report_question(query):
        results = []

        for result in medical_report.results:
            results.append({
                "test_name": result.test_name,
                "value": result.value,
                "unit": result.unit,
                "reference_low": result.reference_low,
                "reference_high": result.reference_high,
                "status": result.status,
                "page": result.page,
            })

        return results, None

    # Specific-test question
    detected_test = find_matching_test(
        query,
        medical_report
    )

    # Follow-up question
    if detected_test is None and previous_test:
        detected_test = previous_test

    if detected_test is None:
        return [], None

    results = []

    for result in medical_report.results:
        if result.test_name.lower() == detected_test.lower():
            results.append({
                "test_name": result.test_name,
                "value": result.value,
                "unit": result.unit,
                "reference_low": result.reference_low,
                "reference_high": result.reference_high,
                "status": result.status,
                "page": result.page,
            })

    return results, detected_test


def retrieve_context(
    query,
    medical_report,
    top_k=5,
    previous_test=None
):
    report_context, detected_test = retrieve_report_context(
        query,
        medical_report,
        previous_test
    )

    # Whole-report question
    if is_whole_report_question(query):
        knowledge_context = []

        return {
            "query": query,
            "detected_test": None,
            "whole_report": True,
            "report_context": report_context,
            "knowledge_context": knowledge_context,
        }

    # Specific-test question
    knowledge_query = query

    if detected_test:
        knowledge_query = f"{detected_test} {query}"

    knowledge_context = search_knowledge(
        knowledge_query,
        top_k=top_k,
        test_name=detected_test
    )

    return {
        "query": query,
        "detected_test": detected_test,
        "whole_report": False,
        "report_context": report_context,
        "knowledge_context": knowledge_context,
    }