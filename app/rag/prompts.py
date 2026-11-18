from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an AI assistant that answers questions based on
    the provided document context.

    Use only the information available in the context.

    If the answer cannot be found in the context, say:

    "I could not find the answer in the provided documents."

    Do not make up information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)


QUERY_REWRITE_PROMPT = ChatPromptTemplate.from_template(
    """
    Rewrite the user's question into a clear and specific
    search query suitable for semantic document retrieval.

    Do not answer the question.

    Original question:
    {question}

    Search query:
    """
)