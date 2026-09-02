import numpy as np

from backend.models import MedicalReport
from backend.knowledge.embeddings import embedding_model


SIMILARITY_THRESHOLD = 0.35


def find_matching_test(query, medical_report: MedicalReport):

    if not medical_report.results:
        return None

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

    best_score = float(
        similarities[best_index]
    )

    if best_score < SIMILARITY_THRESHOLD:
        return None

    return {
        "test_name": test_names[best_index],
        "score": best_score,
    }