
from FlagEmbedding import FlagReranker


_reranker = None


def get_reranker():

    global _reranker

    if _reranker is None:

        _reranker = FlagReranker(
            "BAAI/bge-reranker-v2-m3",
            use_fp16=False
        )

    return _reranker



def rerank(query, documents, top_k=3):

    reranker = get_reranker()


    pairs = []


    for item in documents:

        if isinstance(item, dict):
            doc = item["document"]
        else:
            doc = item


        pairs.append(
            [
                query,
                doc.page_content
            ]
        )


    scores = reranker.compute_score(
        pairs
    )


    if isinstance(scores, float):
        scores = [scores]


    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )


    results = []


    for doc, score in ranked[:top_k]:

        if isinstance(doc, dict):

            results.append(
                {
                    "document": doc["document"],
                    "score": score
                }
            )

        else:

            results.append(
                {
                    "document": doc,
                    "score": score
                }
            )


    return results
