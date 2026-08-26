from app.embeddings.model import EmbeddingModel
from app.config.settings import settings
from app.embeddings.repository import EmbeddingRepository


class EmbeddingService:

    def __init__(self):

        self.model = EmbeddingModel.get_model()

    def generate_embedding(self,text: str) -> list[float]:

        return self.model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()
        
    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:

        vectors = self.model.encode(

            texts,
            batch_size=32,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        return vectors.tolist()
    
    def generate_and_store(self, db, chunk,):
        vector = self.generate_embedding(
            chunk.content
        )

        repository = EmbeddingRepository(db)
        repository.upsert(
            chunk.id,
            settings.EMBEDDING_MODEL,
            vector,
        )
        
    def generate_and_store_batch(self, db, chunks):
        vectors = self.generate_embeddings(
            [
                c.content
                for c in chunks
            ]
        )
        repository = EmbeddingRepository(db)
        rows = []
        for chunk, vector in zip(
            chunks,
            vectors,
        ):
            rows.append(
                {
                    "chunk_id": chunk.id,
                    "model_name": settings.EMBEDDING_MODEL,
                    "embedding": vector,
                }
            )
        repository.bulk_create(rows)