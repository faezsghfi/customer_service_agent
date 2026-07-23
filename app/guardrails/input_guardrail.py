

from app.guardrails.patterns import (
    INJECTION_PATTERNS,
    JAILBREAK_PATTERNS,
    TOXIC_PATTERNS
)

from app.guardrails.pii_detector import detect_pii



def contains_pattern(text, patterns):

    text = text.lower()

    for pattern in patterns:

        if pattern.lower() in text:

            return True

    return False




def validate_input(query):


    if contains_pattern(
        query,
        INJECTION_PATTERNS
    ):

        return {
            "allowed": False,
            "reason": "prompt_injection"
        }



    if contains_pattern(
        query,
        JAILBREAK_PATTERNS
    ):

        return {
            "allowed": False,
            "reason": "jailbreak"
        }



    if contains_pattern(
        query,
        TOXIC_PATTERNS
    ):

        return {
            "allowed": False,
            "reason": "toxicity"
        }




    pii = detect_pii(
        query
    )


    if pii["has_pii"]:

        return {

            "allowed": False,

            "reason": "pii",

            "types": pii["types"]

        }




    return {

        "allowed": True,

        "reason": None

    }
