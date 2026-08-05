from app.embeddings.model import EmbeddingModel


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