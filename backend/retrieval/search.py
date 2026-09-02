import pickle

import faiss

from backend.config import VECTORSTORE_DIR
from backend.knowledge.embeddings import embedding_model


INDEX_PATH = VECTORSTORE_DIR / "medical_knowledge.index"
DOCUMENTS_PATH = VECTORSTORE_DIR / "knowledge_documents.pkl"

index = faiss.read_index(str(INDEX_PATH))

with open(DOCUMENTS_PATH, "rb") as f:
    knowledge_chunks = pickle.load(f)


def search_knowledge(query: str, top_k: int = 5, test_name: str = None):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    search_k = max(top_k * 3, 10)

    scores, indices = index.search(
        query_embedding,
        search_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        document = knowledge_chunks[idx]

        metadata = document.metadata

        if test_name:
            document_test = metadata.get("test_name", "")

            if document_test.lower() != test_name.lower():
                continue

        results.append(
            {
                "score": float(score),
                "content": document.page_content,
                "metadata": metadata,
            }
        )

        if len(results) >= top_k:
            break

    return results