
from app.guardrails.input_guardrail import validate_input


def input_guardrail_node(state):


    messages = state["messages"]


    last_message = messages[-1]


    query = last_message.content



    result = validate_input(
        query
    )



    if not result["allowed"]:


        return {

            "route": "blocked",

            "answer": "متاسفانه نمی‌توانم به این درخواست پاسخ بدهم."

        }



    return {

        "route": "allowed"

    }
