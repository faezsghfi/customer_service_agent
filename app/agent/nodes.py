
import re

from langchain_core.messages import HumanMessage

from app.models.llm import get_llm
from app.agent.router import classify_intent
from app.tools.order_api import get_order_status



def router_node(state):

    last_message = state["messages"][-1]

    route = classify_intent(
        last_message.content
    )

    return {
        "route": route
    }



def chat_node(state):

    llm = get_llm()

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [
            response
        ],
        "answer": response.content
    }



def api_node(state):

    order_id = state.get(
        "order_id",
        ""
    )


    # اگر قبلا ذخیره شده باشد استفاده کن
    if not order_id:

        for msg in state["messages"]:

            ids = re.findall(
                r"\b\d{4}\b",
                msg.content
            )

            if ids:
                order_id = ids[-1]



    if order_id:

        result = get_order_status.invoke(
            {
                "order_id": order_id
            }
        )

    else:

        result = {
            "code": 400,
            "message": "شماره سفارش پیدا نشد."
        }



    return {

        "messages": [
            HumanMessage(
                content=str(result)
            )
        ],

        "tool_result": str(result),

        "order_id": order_id
    }



def rag_node(state):

    return {

        "messages": [
            HumanMessage(
                content="RAG response"
            )
        ]

    }
