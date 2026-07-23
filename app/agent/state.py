
from typing import TypedDict, List, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    # Conversation memory
    messages: Annotated[
        List[BaseMessage],
        add_messages
    ]

    # Router decision
    route: str

    # Retrieved context (RAG)
    context: List[str]

    # Final answer
    answer: str

    # Tool output
    tool_result: str
