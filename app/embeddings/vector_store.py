import chromadb
from app.embeddings.vector_store import collection

client = chromadb.PersistentClient(
    path="storage/chroma"
)

collection = client.get_or_create_collection(
    "documents"
)

def store_chunk(
    chunk_id,
    document_id,
    content,
    embedding,
):

    collection.add(
        ids=[str(chunk_id)],
        embeddings=[embedding],
        documents=[content],
        metadatas=[
            {
                "document_id": str(document_id)
            }
        ],
    )