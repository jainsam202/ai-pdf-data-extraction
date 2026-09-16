from sqlalchemy.orm import Session
from app.models.document_embedding import DocumentEmbedding
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from app.models.document_chunk import DocumentChunk

class EmbeddingRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        chunk_id: int,
        model_name: str,
        embedding: list[float],
    ) -> DocumentEmbedding:

        obj = DocumentEmbedding(
            chunk_id=chunk_id,
            model_name=model_name,
            embedding=embedding,
        )

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get_by_chunk(self, chunk_id: int):
        return (
            self.db.query(
                DocumentEmbedding
            )
            .filter(
                DocumentEmbedding.chunk_id == chunk_id
            )
            .first()
        )
        
    def delete(self, chunk_id: int):
        embedding = self.get_by_chunk(
            chunk_id
        )
        if embedding:
            self.db.delete(embedding)
            self.db.commit()
            
    def upsert(self,chunk_id,model_name,embedding):
        existing = self.get_by_chunk(chunk_id)

        if existing:
            existing.embedding = embedding
            existing.model_name = model_name
            self.db.commit()
            self.db.refresh(existing)
            return existing
        return self.create(
            chunk_id,
            model_name,
            embedding,
        )
        
    def bulk_create(self,rows):
        objects = [
            DocumentEmbedding(
                chunk_id=row["chunk_id"],
                embedding=row["embedding"],
                model_name=row["model_name"],
            )
            for row in rows
        ]
        self.db.add_all(objects)
        self.db.commit()
        return objects
    
    def bulk_upsert(self, rows):

        statement = insert(
            DocumentEmbedding
        ).values(rows)

        statement = statement.on_conflict_do_update(
            index_elements=[
                DocumentEmbedding.chunk_id
            ],
            set_={
                "embedding": statement.excluded.embedding,
                "model_name": statement.excluded.model_name,
            },
        )

        self.db.execute(statement)
        self.db.commit()
      
        
    def search_similar(
    self,
    query_embedding: list[float],
    top_k: int = 5,
    document_id: int | None = None,
    min_score: float = 0.50
    ):
        distance = (DocumentEmbedding.embedding.cosine_distance(query_embedding))
        statement = (
            select(
                DocumentEmbedding.chunk_id,
                DocumentChunk.document_id,
                DocumentChunk.content,
                (1 - distance).label("score"),
            )
            .join(
                DocumentChunk,
                DocumentChunk.id
                == DocumentEmbedding.chunk_id,
            )
            .where((1 - distance) >= min_score)
            .order_by(distance)
            .limit(top_k)
        )

        if document_id is not None:
            statement = statement.where(
                DocumentChunk.document_id == document_id
            )

        return self.db.execute(statement).all()