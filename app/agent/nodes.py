
from langchain_core.messages import HumanMessage

from app.models.llm import get_llm
from app.agent.router import classify_intent
from app.tools.order_api import get_order_status


def router_node(state):
    """
    Decide next path.
    """

    last_message = state["messages"][-1]

    route = classify_intent(
        last_message.content
    )

    return {
        "route": route
    }



def chat_node(state):
    """
    Normal conversation.
    """

    llm = get_llm()

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [
            response
        ]
    }



def api_node(state):
    """
    Call external order API tool.
    """

    user_message = state["messages"][-1].content


    order_id = None

    for token in user_message.split():
        if token.isdigit():
            order_id = token


    if order_id is None:

        result = "شماره سفارش پیدا نشد."

    else:

        result = get_order_status.invoke(
            {
                "order_id": order_id
            }
        )


    return {
        "messages": [
            HumanMessage(
                content=str(result)
            )
        ],

        "tool_result": str(result)
    }



def rag_node(state):
    """
    Temporary node.
    Will be replaced in Advanced RAG phase.
    """

    return {
        "messages":[
            HumanMessage(
                content=
                "RAG module is not implemented yet."
            )
        ]
    }
