import re
from langchain_core.messages import AIMessage
from app.rag.pipeline import run_rag

from app.models.llm import get_llm
from app.agent.router import classify_intent
from app.tools.order_api import get_order_status

from app.core.logger import (
    section,
    thought,
    action,
    observation,
    success,
    warning,
    error
)

def router_node(state):

    section("ROUTER NODE")
    thought("Analyzing user intent to decide the next execution path.")

    last_message = state["messages"][-1]

    observation(f"User message: {last_message.content}")
    action("Classifying user intent")
    route = classify_intent(last_message.content)
    observation(f"Selected route: {route}")


    if route in ["chat","api","rag"]:
        success(f"Routing decision accepted: {route}")
    else:
        warning(f"Unknown route returned: {route}")
        route = "chat"

    success("ROUTER NODE finished")

    return {"route": route}


def chat_node(state):

    section("CHAT NODE")
    thought("User request does not require external tools, generating a direct response with LLM.")
    observation(f"Messages count: {len(state['messages'])}")
    action("Calling LLM")

    llm = get_llm()

    response = llm.invoke(state["messages"])

    success("LLM response generated successfully")
    observation(f"Response length: {len(response.content.split())} words")
    success("CHAT NODE finished")


    return {"messages": [response],"answer": response.content}

def api_node(state):

    section("API NODE")
    thought("User request requires external order information, checking order_id before calling API.")

    # آخرین پیام کاربر
    last_message = state["messages"][-1].content

    observation(f"User message: {last_message}")

    # پیدا کردن شماره سفارش
    action("Searching for order_id inside the last message")


    ids = re.findall(r"\d{4}",last_message)


    if ids:
        order_id = ids[-1]
        observation(f"Order ID found in message: {order_id}")
    else:
        warning("No order_id found in message, falling back to memory")
        order_id = state.get("order_id")
        observation(f"Order ID from memory: {order_id}")

    # اگر هیچ شماره سفارشی پیدا نشد
    if not order_id:
        warning("No order_id available (neither in message nor memory)")
        return {"messages": [AIMessage(content="لطفاً شماره سفارش را وارد کنید.")]}



    # آماده سازی درخواست API
    action(
        "Preparing API request"
    )


    observation(
        f"API parameters: order_id={order_id}"
    )



    # فراخوانی API
    action(
        "Calling get_order_status tool"
    )


    try:

        result = get_order_status.invoke(
            {
                "order_id": order_id
            }
        )


        success(
            "get_order_status tool executed successfully"
        )


        observation(
            f"Tool result: {result}"
        )



    except Exception as e:


        error(
            f"API call failed: {str(e)}"
        )


        return {

            "messages": [
                AIMessage(
                    content="در حال حاضر امکان دریافت وضعیت سفارش وجود ندارد."
                )
            ],

            "tool_result": None,

            "order_id": order_id

        }



    success(
        "API NODE finished"
    )



    return {

        "messages": [
            AIMessage(
                content=str(result)
            )
        ],

        "tool_result": result,

        "order_id": order_id

    }

def rag_node(state):

    section("RAG NODE")

    thought("Knowledge Base is required to answer this question.")

    question = state["messages"][-1].content

    observation(f"Question: {question}")
    action("Executing RAG Pipeline")

    result = run_rag(question)

    success("RAG Pipeline completed")
    observation(f"Retrieved Context Chunks: {len(result['context'])}")
    success("Answer is ready")
    return {
        "messages": [AIMessage(content=result["answer"])],"answer": result["answer"],"context": result["context"]}
