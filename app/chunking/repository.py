from app.models.document_chunk import DocumentChunk


class ChunkRepository:

    def __init__(self, db):

        self.db = db

    def save_chunk(

        self,

        document_id,

        index,

        content,

        content_hash,

    ):

        chunk = DocumentChunk(

            document_id=document_id,

            chunk_index=index,

            content=content,

            content_hash=content_hash,
        )

        self.db.add(chunk)

        self.db.commit()