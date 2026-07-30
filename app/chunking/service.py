from app.chunking.hasher import ChunkHasher
from app.chunking.metadata import MetadataExtractor
from app.chunking.repository import ChunkRepository
from app.chunking.splitter import ChunkSplitter


class ChunkService:

    def __init__(self, db):
        self.repository = ChunkRepository(db)

    def process(
        self,
        document_id,
        text,
    ):
        chunks = ChunkSplitter.split(text)

        for index, chunk in enumerate(chunks):

            metadata = MetadataExtractor.extract(chunk)

            content_hash = ChunkHasher.hash(chunk)

            self.repository.save_chunk(

                document_id=document_id,

                index=index,

                content=chunk,

                content_hash=content_hash,
            )

        return len(chunks)