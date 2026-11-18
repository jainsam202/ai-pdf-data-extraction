import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.graph.workflow import build_rag_graph
from app.llm.factory import get_llm
from app.rag.retriever import PgVectorRetriever
from app.rag.schemas import RAGQuery, RAGResponse
from app.rag.service import RAGService
from langchain_google_genai.chat_models import GoogleAPIError


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post("/query", response_model=RAGResponse)
def query_rag(
    request: RAGQuery,
    db: Session = Depends(get_db),
):
    retriever = PgVectorRetriever(
        db=db,
        document_id=request.document_id,
    )

    llm = get_llm()
    graph = build_rag_graph(retriever, llm)
    service = RAGService(graph)

    try:
        return service.ask(
            question=request.question,
            document_id=request.document_id,
        )
    except GoogleAPIError:
        logger.exception("Gemini failed while processing the RAG query")
        raise HTTPException(
            status_code=503,
            detail="The answer-generation service is temporarily unavailable. Please try again.",
        )
