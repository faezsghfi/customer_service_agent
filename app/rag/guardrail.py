
def validate_context(results, threshold=0.5):

    """
    RAG relevance and out-of-domain guardrail.
    """


    if not results:

        return {
            "allowed": False,
            "context": []
        }



    context = []



    # -------------------------
    # Reranker output
    # -------------------------

    if isinstance(results[0], dict):


        best_score = results[0].get(
            "score",
            0
        )


        if best_score < threshold:

            return {
                "allowed": False,
                "context": []
            }



        for item in results:

            doc = item.get(
                "document"
            )


            if doc:

                context.append(
                    doc.page_content
                )



    # -------------------------
    # Parent context strings
    # -------------------------

    elif isinstance(results[0], str):


        for item in results:

            if len(item.strip()) > 20:

                context.append(item)



    # -------------------------
    # LangChain Documents
    # -------------------------

    else:


        for doc in results:

            if hasattr(
                doc,
                "page_content"
            ):

                context.append(
                    doc.page_content
                )



    # -------------------------
    # Final validation
    # -------------------------

    if not context:

        return {
            "allowed": False,
            "context": []
        }



    total_length = sum(
        len(x)
        for x in context
    )


    if total_length < 50:

        return {
            "allowed": False,
            "context": []
        }



    return {

        "allowed": True,

        "context": context

    }
