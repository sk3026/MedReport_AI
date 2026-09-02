from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config import CONFIG
from backend.knowledge.documents import load_medical_documents


def create_knowledge_chunks():
    documents = load_medical_documents()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CONFIG["chunk_size"],
        chunk_overlap=CONFIG["chunk_overlap"],
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        topic = chunk.metadata.get("topic", "Unknown")

        chunk.metadata.update(
            {
                "chunk_id": i,
                "topic": topic,
                "test_name": topic,
                "document_type": "medical_knowledge",
                "source": "MedReport AI Medical Knowledge Base",
            }
        )

    return chunks