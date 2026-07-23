
from app.models.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "سلام. خودت را معرفی کن."
)

print(response.content)
