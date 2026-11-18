class RAGService:

    def __init__(self, graph):
        self.graph = graph

    def ask(
        self,
        question: str,
        document_id: int | None = None,
    ):

        state = {
            "question": question,
            "document_id": document_id,
            "retrieval_attempts": 0,
        }

        result = self.graph.invoke(state)

        return {
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
        }