
from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from langchain_core.documents import Document



class AgentState(TypedDict):
    """
    Shared state between LangGraph nodes.
    """


    # Conversation history
    messages: Annotated[
        list,
        add_messages
    ]


    # Router decision
    route: Literal[
        "chat",
        "rag",
        "api"
    ]


    # Retrieved documents from vector database
    retrieved_docs: list[Document]


    # External tool result
    tool_result: str
