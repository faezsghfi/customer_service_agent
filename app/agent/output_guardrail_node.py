

def output_guardrail_node(state):

    answer = state.get(
        "answer",
        ""
    )


    context = state.get(
        "context",
        []
    )


    if not answer:

        return {
            "answer": "پاسخی تولید نشد."
        }



    if not context:

        return {
            "answer": "اطلاعات کافی در پایگاه دانش موجود نیست."
        }



    answer_words = set(
        answer.split()
    )


    context_text = " ".join(
        context
    )


    context_words = set(
        context_text.split()
    )


    overlap = (
        len(answer_words & context_words)
        /
        max(len(answer_words), 1)
    )



    # حداقل 30 درصد کلمات جواب باید
    # در context وجود داشته باشد

    if overlap < 0.3:

        return {
            "answer":
            "اطلاعات کافی در پایگاه دانش موجود نیست."
        }



    return {
        "answer": answer
    }
