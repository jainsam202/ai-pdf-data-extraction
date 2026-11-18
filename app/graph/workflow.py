
from langgraph.graph import StateGraph, START, END
from app.graph.state import GraphState
from app.graph.nodes import (
    retrieve_documents,
    build_context,
    check_relevance,
    generate_answer,
)


def build_rag_graph(retriever, llm):
    graph = StateGraph(GraphState)

    graph.add_node("retrieve",lambda state: retrieve_documents(state, retriever))
    graph.add_node("build_context", build_context)
    graph.add_node("check_relevance", check_relevance)
    graph.add_node("generate",lambda state: generate_answer(state, llm))
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "build_context")
    graph.add_edge("build_context", "check_relevance")
    graph.add_edge("check_relevance", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
