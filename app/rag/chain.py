

from app.rag.prompt import RAG_PROMPT


def build_context(results):

    return "\n\n".join(
        [
            item["document"].page_content
            for item in results
        ]
    )


def create_rag_prompt(
    results,
    question
):

    context = build_context(results)


    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )


    return prompt
