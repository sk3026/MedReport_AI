from backend.generation.llm import generate_answer
from backend.generation.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from backend.safety.checker import check_response


def generate_safe_response(question, rag_context):

    user_prompt = build_user_prompt(
        question,
        rag_context
    )

    answer = generate_answer(
        SYSTEM_PROMPT,
        user_prompt
    )

    safety_result = check_response(answer)

    if not safety_result["safe"]:
        return {
            "answer": (
                "I can provide general educational information "
                "about laboratory results, but I cannot provide "
                "diagnoses, prescriptions, medication instructions, "
                "or other clinical decisions."
            ),
            "safe": False,
            "violations": safety_result["violations"],
        }

    return {
        "answer": answer,
        "safe": True,
        "violations": [],
    }