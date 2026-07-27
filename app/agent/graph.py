
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.agent.state import AgentState

from app.agent.nodes import (
    router_node,
    chat_node,
    api_node,
    rag_node
)

from app.agent.guardrail_node import input_guardrail_node
from app.agent.output_guardrail_node import output_guardrail_node


memory = MemorySaver()


def build_graph():

    workflow = StateGraph(
        AgentState
    )


    workflow.add_node(
        "guardrail",
        input_guardrail_node
    )

    workflow.add_node(
        "router",
        router_node
    )

    workflow.add_node(
        "chat",
        chat_node
    )

    workflow.add_node(
        "api",
        api_node
    )

    workflow.add_node(
        "rag",
        rag_node
    )

    workflow.add_node(
        "output_guardrail",
        output_guardrail_node
    )


    workflow.add_edge(
        START,
        "guardrail"
    )


    workflow.add_conditional_edges(
        "guardrail",
        lambda state: state["route"],
        {
            "allowed": "router",
            "blocked": END
        }
)


    workflow.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "chat": "chat",
            "api": "api",
            "rag": "rag"
        }
    )


    workflow.add_edge(
        "chat",
        END
    )

    workflow.add_edge(
        "api",
        END
    )

    workflow.add_edge(
        "rag",
        "output_guardrail"
    )

    workflow.add_edge(
        "output_guardrail",
        END
    )


    return workflow.compile(
        checkpointer=memory
    )
