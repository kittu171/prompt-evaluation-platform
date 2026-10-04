import os

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from evaluator import (
    evaluate_all,
    calculate_overall_score
)


# =========================================================
# LLM
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

class ImprovedPrompt(BaseModel):

    prompt: str = Field(
        description="The final improved prompt only."
    )


structured_llm = llm.with_structured_output(
    ImprovedPrompt
)


# =========================================================
# GENERATE PROMPT VARIANTS
# =========================================================

def generate_prompt_variants(
    original_prompt: str
):

    optimization_prompt = f"""
You are a prompt engineering expert.

The goal is to improve prompts for Generative AI applications.

Important project context:

In this project, RAG means Retrieval-Augmented Generation.
RAG is a technique that retrieves relevant information
before generating an answer.

Improve the following user prompt by creating 3 different
prompt versions.

Original Prompt:
{original_prompt}

Rules:

1. Preserve the original meaning.
2. Do not change the user's intended task.
3. Do not introduce unrelated meanings.
4. If a technical term is ambiguous, use the project context.
5. Make each version clearer and more specific.
6. Version 1 should be simple and clear.
7. Version 2 should contain detailed instructions.
8. Version 3 should contain precise output constraints.
9. Keep the prompts suitable for a Generative AI system.

Create:

Version 1:
A simple and clear version.

Version 2:
A detailed version with specific instructions.

Version 3:
A highly precise version with clear output constraints.

Return the result exactly in this format:

Version 1:
<improved prompt>

Version 2:
<improved prompt>

Version 3:
<improved prompt>
"""

    result = llm.invoke(
        optimization_prompt
    )

    return result.content.strip()


# =========================================================
# EXTRACT PROMPT VARIANTS
# =========================================================

def extract_prompt_variants(
    variants_text: str
):

    variants = {}

    current_version = None

    for line in variants_text.splitlines():

        line = line.strip()

        if line.startswith("Version 1:"):

            current_version = "Version 1"
            variants[current_version] = []

        elif line.startswith("Version 2:"):

            current_version = "Version 2"
            variants[current_version] = []

        elif line.startswith("Version 3:"):

            current_version = "Version 3"
            variants[current_version] = []

        elif current_version and line:

            variants[current_version].append(
                line
            )

    for version in variants:

        variants[version] = " ".join(
            variants[version]
        )

    return variants


# =========================================================
# GENERATE AI RESPONSE
# =========================================================

def generate_response(
    prompt: str
):

    result = llm.invoke(
        prompt
    )

    return result.content.strip()


# =========================================================
# SELECT BEST PROMPT
# =========================================================

def select_best_prompt(
    evaluation_results
):

    best_version = None
    best_score = -1

    for version, data in evaluation_results.items():

        score = data["overall_score"]

        if score > best_score:

            best_score = score
            best_version = version

    return best_version, best_score


# =========================================================
# IMPROVE BEST PROMPT
# =========================================================

def improve_best_prompt(
    best_prompt: str,
    evaluation_results
):

    weak_criteria = []

    for criterion, evaluation in evaluation_results.items():

        if evaluation.score < 8:

            weak_criteria.append(
                f"{criterion}: "
                f"{evaluation.score}/10 - "
                f"{evaluation.explanation}"
            )

    if not weak_criteria:

        weak_criteria_text = (
            "No major weaknesses were found. "
            "Make only small improvements if useful."
        )

    else:

        weak_criteria_text = "\n".join(
            weak_criteria
        )

    improvement_prompt = f"""
You are an expert prompt engineer.

Improve the following AI prompt based on its evaluation.

Best Prompt:
{best_prompt}

Evaluation Weaknesses:
{weak_criteria_text}

Rules:

1. Preserve the original intent.
2. Do not change the user's task.
3. Do not add unrelated requirements.
4. Improve only the identified weaknesses.
5. Make the instructions clear.
6. Make the expected output clear.
7. Keep the prompt practical for a Generative AI system.
8. Return ONLY the final improved prompt.
9. Do not return explanations.
10. Do not return evaluation changes.
11. Do not add labels such as "Improved Prompt:".
"""

    result = structured_llm.invoke(
        improvement_prompt
    )

    return result.prompt.strip()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    original_prompt = "Explain RAG."

    # -----------------------------------------------------
    # STEP 1: Generate Prompt Variants
    # -----------------------------------------------------

    variants_text = generate_prompt_variants(
        original_prompt
    )

    variants = extract_prompt_variants(
        variants_text
    )

    print("\n" + "=" * 50)
    print("PROMPT VARIANTS")
    print("=" * 50)

    for version, prompt in variants.items():

        print(f"\n{version}:")
        print(prompt)

    # -----------------------------------------------------
    # STEP 2: Generate Responses
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("GENERATED RESPONSES")
    print("=" * 50)

    responses = {}

    for version, prompt in variants.items():

        response = generate_response(
            prompt
        )

        responses[version] = response

        print(f"\n{version}")

        print("\nPrompt:")
        print(prompt)

        print("\nAI Response:")
        print(response)

    # -----------------------------------------------------
    # STEP 3: Evaluate Responses
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("PROMPT EVALUATION")
    print("=" * 50)

    evaluation_results = {}

    for version, prompt in variants.items():

        response = responses[version]

        print(
            f"\nEvaluating {version}..."
        )

        results = evaluate_all(
            prompt,
            response
        )

        overall_score = calculate_overall_score(
            results
        )

        evaluation_results[version] = {
            "results": results,
            "overall_score": overall_score
        }

        print(
            f"\n{version} Overall Score: "
            f"{overall_score}"
        )

    # -----------------------------------------------------
    # STEP 4: Compare Prompts
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("FINAL COMPARISON")
    print("=" * 50)

    for version, data in evaluation_results.items():

        print(
            f"{version}: "
            f"{data['overall_score']}/10"
        )

    # -----------------------------------------------------
    # STEP 5: Select Best Prompt
    # -----------------------------------------------------

    best_version, best_score = select_best_prompt(
        evaluation_results
    )

    best_prompt = variants[
        best_version
    ]

    print("\n" + "=" * 50)
    print("BEST PROMPT")
    print("=" * 50)

    print(
        f"Best Prompt: {best_version}"
    )

    print(
        f"Best Score: {best_score}/10"
    )

    print("\nSelected Prompt:")

    print(
        best_prompt
    )

    # -----------------------------------------------------
    # STEP 6: Improve Best Prompt
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("FINAL IMPROVED PROMPT")
    print("=" * 50)

    best_evaluation = evaluation_results[
        best_version
    ]["results"]

    final_improved_prompt = improve_best_prompt(
        best_prompt,
        best_evaluation
    )

    print(
        "\nFinal Improved Prompt:"
    )

    print(
        final_improved_prompt
    )