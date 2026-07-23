
from langchain_openai import ChatOpenAI

from app.config import settings



def get_llm():
    """
    LLM factory.

    Central place for creating LLM instances.
    """


    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0
    )


    return llm
