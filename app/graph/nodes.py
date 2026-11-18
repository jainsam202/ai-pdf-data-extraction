from app.graph.state import GraphState
from app.rag.prompts import RAG_PROMPT, QUERY_REWRITE_PROMPT
import logging
import time

logger = logging.getLogger(__name__)

def _content_to_text(content) -> str:
    """Convert an LLM response's content into a plain string."""
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
            elif isinstance(block, dict):
                text = block.get("text")
                if isinstance(text, str):
                    text_parts.append(text)

        return "\n".join(text_parts).strip()

    return str(content).strip()


def retrieve_documents(state: GraphState, retriever) -> GraphState:
    question = state.get("rewritten_question", state["question"])
    documents = retriever.invoke(question)

    logger.info(
        "RETRIEVAL: question=%r, document_id=%s, documents_found=%d",
        question,
        state.get("document_id"),
        len(documents),
    )

    for document in documents:
        logger.info(
            "RETRIEVAL: chunk_id=%s, score=%s",
            document.metadata.get("chunk_id"),
            document.metadata.get("score"),
        )

    return {
        "documents": documents,
        "retrieval_attempts": state.get("retrieval_attempts", 0) + 1,
    }


def build_context(state: GraphState) -> GraphState:
    documents = state.get("documents", [])

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return {
        "context": context,
    }


def check_relevance(state: GraphState) -> GraphState:
    documents = state.get("documents", [])
    relevant = len(documents) > 0

    return {
        "relevant": relevant,
    }


def generate_answer(state: GraphState, llm) -> GraphState:
    messages = RAG_PROMPT.invoke(
        {
            "context": state.get("context", ""),
            "question": state["question"],
        }
    )

    start_time = time.perf_counter()
    logger.info("GENERATE_ANSWER: Gemini request started")

    try:
        response = llm.invoke(messages)
    except Exception:
        logger.exception("GENERATE_ANSWER: Gemini request failed")
        raise

    elapsed = time.perf_counter() - start_time
    logger.info("GENERATE_ANSWER: Gemini request completed in %.2f seconds",
        elapsed,
    )

    answer = _content_to_text(response.content)

    documents = state.get("documents", [])

    sources = [
        {
            "chunk_id": document.metadata.get("chunk_id"),
            "document_id": document.metadata.get("document_id"),
            "score": document.metadata.get("score"),
        }
        for document in documents
    ]

    return {
        "answer": answer,
        "sources": sources,
    }



def rewrite_query(state: GraphState, llm) -> GraphState:
    messages = QUERY_REWRITE_PROMPT.invoke(
        {
            "question": state["question"],
        }
    )
    logger.info("REWRITE_QUERY: started")
    start = time.perf_counter()

    response = llm.invoke(messages)
    logger.info("REWRITE_QUERY: completed in %.2f seconds",
        time.perf_counter() - start
    )

    return {
        "rewritten_question": _content_to_text(response.content),
    }
