

def reciprocal_rank_fusion(
    dense_results,
    sparse_results,
    k=60
):

    scores = {}

    docs = {}


    for rank, doc in enumerate(dense_results):

        key = doc.page_content

        docs[key] = doc

        scores[key] = scores.get(key,0) + 1/(rank+k)



    for rank, doc in enumerate(sparse_results):

        key = doc.page_content

        docs[key] = doc

        scores[key] = scores.get(key,0) + 1/(rank+k)



    ranked = sorted(
        scores.items(),
        key=lambda x:x[1],
        reverse=True
    )


    return [
        docs[text]
        for text,score in ranked
    ]
