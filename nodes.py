
from langchain_core.messages import HumanMessage

from app.models.llm import get_llm
from app.agent.router import classify_intent
from app.tools.order_api import get_order_status

from app.rag.pipeline import run_rag


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
    Advanced RAG node.

    Flow:
    Query
      |
    Hybrid Retrieval
      |
    Reranker
      |
    Guardrail
      |
    LLM Answer
    """


    query = state["messages"][-1].content


    answer = run_rag(
        query
    )


    return {
        "messages": [
            HumanMessage(
                content=answer
            )
        ]
    }
