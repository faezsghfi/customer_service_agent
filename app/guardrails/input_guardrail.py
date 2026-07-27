

from app.guardrails.patterns import (
    INJECTION_PATTERNS,
    JAILBREAK_PATTERNS,
    TOXIC_PATTERNS
)

from app.guardrails.pii_detector import detect_pii



import re


def normalize_text(text: str) -> str:
    text = text.lower()

    text = text.replace("ي", "ی")
    text = text.replace("ك", "ک")
    text = text.replace("‌", " ")      # حذف نیم‌فاصله
    text = re.sub(r"\s+", " ", text)   # یکی کردن فاصله‌ها

    return text.strip()


def contains_pattern(text: str, patterns: list[str]) -> bool:
    """
    Check whether the input text matches
    any suspicious regex pattern.
    """

    text = normalize_text(text)

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False




def validate_input(query):
    if contains_pattern(query,INJECTION_PATTERNS):
        return {"allowed": False,"reason": "prompt_injection"}

    if contains_pattern(query,JAILBREAK_PATTERNS):
        return {"allowed": False,"reason": "jailbreak"}

    if contains_pattern(query,TOXIC_PATTERNS):
        return {"allowed": False,"reason": "toxicity"}
    
    pii = detect_pii(query)

    if pii["has_pii"]:
        return {"allowed": False,"reason": "pii","types": pii["types"]}
    
    return {"allowed": True,"reason": None }
