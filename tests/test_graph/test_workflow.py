from app.graph.edges import route_after_relevance


def test_relevant_documents_route_to_generate():

    state = {
        "relevant": True,
        "retrieval_attempts": 1,
    }

    assert route_after_relevance(state) == "generate"


def test_irrelevant_documents_route_to_rewrite():

    state = {
        "relevant": False,
        "retrieval_attempts": 1,
    }

    assert route_after_relevance(state) == "rewrite"


def test_max_attempts_route_to_generate():

    state = {
        "relevant": False,
        "retrieval_attempts": 2,
    }

    assert route_after_relevance(state) == "generate"