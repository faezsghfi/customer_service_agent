from app.core.logger import (
    section,
    thought,
    action,
    observation,
    success,
    warning
)

def output_guardrail_node(state):

    section("OUTPUT GUARDRAIL")
    thought("Checking generated answer against retrieved context to prevent unsupported responses.")

    answer = state.get("answer","")

    context = state.get("context",[])

    observation(f"Answer length: {len(answer.split())} words")
    observation(f"Context chunks: {len(context)}")

    # بررسی وجود جواب
    action("Checking generated answer")
    if not answer:
        warning("No answer generated")
        return {"answer": "پاسخی تولید نشد."}

    # بررسی وجود Context
    action("Checking retrieved context")

    if not context:
        warning("No context available for validation")
        return {"answer": "اطلاعات کافی در پایگاه دانش موجود نیست."}


    # محاسبه میزان تطابق جواب با Context
    action("Calculating answer-context overlap")

    answer_words = set(answer.split())
    context_text = " ".join(context)
    context_words = set(context_text.split())
    overlap = (len(answer_words & context_words)/max(len(answer_words), 1))

    observation(f"Answer-context overlap score: {overlap:.2f}")

    # تصمیم گیری Guardrail
    action("Validating answer grounding")

    if overlap < 0.3:
        warning("Answer is not sufficiently grounded in context")
        return {"answer":"اطلاعات کافی در پایگاه دانش موجود نیست."}
    success("Output guardrail passed")
    return {"answer": answer}