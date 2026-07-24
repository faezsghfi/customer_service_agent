
from typing import TypedDict, List, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    messages: Annotated[
        List[BaseMessage],
        add_messages
    ]

    route: str

    context: List[str]

    answer: str

    tool_result: str

    order_id: str
