
from FlagEmbedding import FlagReranker


reranker = FlagReranker(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=False
)


def rerank(query, documents, top_k=3):

    pairs = [
        [
            query,
            doc.page_content
        ]
        for doc in documents
    ]

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


    return [
        {
            "document": doc,
            "score": score
        }
        for doc, score in ranked[:top_k]
    ]
