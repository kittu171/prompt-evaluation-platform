import os

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


# =========================================================
# LLM CONFIGURATION
# =========================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url=OLLAMA_BASE_URL
)


# =========================================================
# STRUCTURED OUTPUT MODEL
# =========================================================

class EvaluationResult(BaseModel):

    score: float = Field(
        ge=1,
        le=10
    )

    explanation: str


structured_llm = llm.with_structured_output(
    EvaluationResult
)


# =========================================================
# EVALUATION CRITERIA
# =========================================================

CRITERIA = [
    "Correctness",
    "Relevance",
    "Clarity",
    "Conciseness",
    "Instruction Following"
]


# =========================================================
# EVALUATE ONE CRITERION
# =========================================================

def evaluate_response(
    prompt: str,
    response: str,
    criteria: str
):

    evaluation_prompt = f"""
You are an AI response evaluator.

Evaluate the AI response using ONLY the given criterion.

Criterion:
{criteria}

User Prompt:
{prompt}

AI Response:
{response}

Return a score from 1 to 10 and a short explanation.
Do not evaluate any other criterion.
"""

    result = structured_llm.invoke(
        evaluation_prompt
    )

    return result


# =========================================================
# EVALUATE ALL CRITERIA
# =========================================================

def evaluate_all(
    prompt: str,
    response: str
):

    results = {}

    for criterion in CRITERIA:

        print(
            f"\nEvaluating: {criterion}"
        )

        evaluation = evaluate_response(
            prompt,
            response,
            criterion
        )

        results[criterion] = evaluation

    return results


# =========================================================
# CALCULATE OVERALL SCORE
# =========================================================

def calculate_overall_score(
    results
):

    scores = [
        evaluation.score
        for evaluation in results.values()
    ]

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2
    )


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    prompt = (
        "Explain RAG in 3 simple points."
    )

    response = """
    RAG stands for Retrieval-Augmented Generation.
    It retrieves relevant information before generating
    an answer.
    RAG helps reduce hallucinations by grounding answers
    in retrieved data.
    """

    results = evaluate_all(
        prompt,
        response
    )

    print("\n" + "=" * 50)
    print("FINAL EVALUATION")
    print("=" * 50)

    for criterion, evaluation in results.items():

        print(f"\n{criterion}:")
        print(
            f"Score: {evaluation.score}"
        )
        print(
            f"Explanation: {evaluation.explanation}"
        )

    overall_score = calculate_overall_score(
        results
    )

    print("\nOverall Score:")
    print(overall_score)