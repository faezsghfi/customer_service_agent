
from app.guardrails.input_guardrail import validate_input
from app.core.logger import (
    section,
    thought,
    action,
    observation,
    success,
    warning
)

def input_guardrail_node(state):

    section("INPUT GUARDRAIL NODE")
    messages = state["messages"]


    last_message = messages[-1]


    query = last_message.content

    observation(f"User query: {query}")
    action("Validating input against guardrail rules")

    result = validate_input(
        query
    )

    observation(f"Validation result: {result}")

    if not result["allowed"]:

        warning(f"Input blocked by guardrail. Reason: {result.get('reason', 'unspecified')}")

        return {

            "route": "blocked",

            "answer": "متاسفانه نمی‌توانم به این درخواست پاسخ بدهم."

        }

    success("Input passed guardrail checks")

    return {

        "route": "allowed"

    }
