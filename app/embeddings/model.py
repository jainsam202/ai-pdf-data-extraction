from sentence_transformers import SentenceTransformer
from app.config.settings import settings


class EmbeddingModel:

    _instance = None

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            cls._instance = SentenceTransformer(settings.EMBEDDING_MODEL)
        return cls._instance

    @classmethod
    def embed_query(cls, text: str) -> list[float]:

        model = cls.get_model()
        embedding = model.encode(text,normalize_embeddings=True,)
        return embedding.tolist()