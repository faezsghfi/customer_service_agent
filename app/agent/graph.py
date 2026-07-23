
from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.agent.state import AgentState

from app.agent.nodes import (
    router_node,
    chat_node,
    api_node,
    rag_node
)



def build_graph():

    graph = StateGraph(
        AgentState
    )


    # Nodes

    graph.add_node(
        "router",
        router_node
    )


    graph.add_node(
        "chat",
        chat_node
    )


    graph.add_node(
        "api",
        api_node
    )


    graph.add_node(
        "rag",
        rag_node
    )


    # Start

    graph.add_edge(
        START,
        "router"
    )


    # Conditional routing

    graph.add_conditional_edges(
        "router",

        lambda state: state["route"],

        {
            "chat":"chat",
            "api":"api",
            "rag":"rag"
        }
    )


    # End edges

    graph.add_edge(
        "chat",
        END
    )

    graph.add_edge(
        "api",
        END
    )

    graph.add_edge(
        "rag",
        END
    )


    return graph.compile()
