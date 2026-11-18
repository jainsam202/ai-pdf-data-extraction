from app.graph.state import GraphState


def route_after_relevance(state: GraphState) -> str:

    if state.get("relevant", False):
        return "generate"

    attempts = state.get(
        "retrieval_attempts",
        0,
    )

    if attempts >= 2:
        return "generate"

    return "rewrite"