
from typing import Literal

from pydantic import BaseModel

from langchain_core.messages import SystemMessage, HumanMessage

from app.models.llm import get_llm
from app.agent.prompts import ROUTER_SYSTEM_PROMPT



class RouterDecision(BaseModel):
    """
    Structured output of router.
    """

    route: Literal[
        "chat",
        "rag",
        "api"
    ]



def classify_intent(message: str) -> str:
    """
    Classify user message into a route.
    """


    llm = get_llm()


    structured_llm = llm.with_structured_output(
        RouterDecision
    )


    response = structured_llm.invoke(
        [
            SystemMessage(
                content=ROUTER_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=message
            )
        ]
    )


    return response.route
