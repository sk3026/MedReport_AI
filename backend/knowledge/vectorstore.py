import pickle

import faiss

from backend.config import VECTORSTORE_DIR
from backend.knowledge.chunking import create_knowledge_chunks
from backend.knowledge.embeddings import generate_embeddings


def build_vector_store():
    chunks = create_knowledge_chunks()

    texts = [chunk.page_content for chunk in chunks]

    embeddings = generate_embeddings(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings.astype("float32"))

    index_path = VECTORSTORE_DIR / "medical_knowledge.index"
    documents_path = VECTORSTORE_DIR / "knowledge_documents.pkl"

    faiss.write_index(index, str(index_path))

    with open(documents_path, "wb") as f:
        pickle.dump(chunks, f)

    return index, chunks