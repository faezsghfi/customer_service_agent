import gradio as gr
from langchain_core.messages import HumanMessage

from app.agent.graph import build_graph

from app.core.logger import (
    section,
    observation
)


graph = build_graph()


def respond(message, history):

    section("NEW REQUEST")

    observation(
        f"User message: {message}"
    )


    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=message
                )
            ]
        },
        config={
            "configurable": {
                "thread_id": "demo-user"
            }
        }
    )


    route = result.get(
        "route",
        ""
    )


    tool_result = result.get(
        "tool_result",
        ""
    )


    if route == "api":

        answer = f"""
✅ سفارش شما بررسی شد.

📦 نتیجه سفارش:

{tool_result}
"""


    else:

        answer = f"""
🤖 پاسخ دستیار:

{result.get("answer", tool_result)}
"""


    return answer



demo = gr.ChatInterface(
    fn=respond,
    title="🤖 Customer Support Agent",
    description="AI Agent with Thought / Action / Observation"
)



demo.launch(
    share=True
)