

def validate_context(
    reranked_results,
    score_threshold=0
):

    """
    Validate retrieved documents before sending to LLM.
    Prevent hallucination when context is weak.
    """

    if not reranked_results:
        return {
            "allowed": False,
            "reason": "No documents found"
        }


    best_score = reranked_results[0]["score"]


    if best_score < score_threshold:

        return {
            "allowed": False,
            "reason": "Low relevance score"
        }


    return {
        "allowed": True,
        "context": [
            item["document"].page_content
            for item in reranked_results
        ]
    }
