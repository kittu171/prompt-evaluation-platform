from fastapi import FastAPI
from pydantic import BaseModel

from prompt_optimizer import (
    generate_prompt_variants,
    extract_prompt_variants,
    generate_response,
    select_best_prompt,
    improve_best_prompt
)

from evaluator import (
    evaluate_all,
    calculate_overall_score
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Prompt Evaluation & Optimization Platform",
    description="Evaluate, compare and optimize AI prompts.",
    version="1.0.0"
)


# =========================================================
# REQUEST MODEL
# =========================================================

class PromptRequest(BaseModel):

    prompt: str


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================================================
# OPTIMIZE PROMPT
# =========================================================

@app.post("/optimize")
def optimize_prompt(
    request: PromptRequest
):

    # -----------------------------------------------------
    # STEP 1: Validate Input
    # -----------------------------------------------------

    original_prompt = request.prompt.strip()

    if not original_prompt:

        return {
            "error": "Prompt cannot be empty."
        }

    if len(original_prompt) > 1000:

        return {
            "error": (
                "Prompt is too long. "
                "Maximum 1000 characters allowed."
            )
        }

    # -----------------------------------------------------
    # STEP 2: Generate Prompt Variants
    # -----------------------------------------------------

    variants_text = generate_prompt_variants(
        original_prompt
    )

    variants = extract_prompt_variants(
        variants_text
    )

    if not variants:

        return {
            "error": "Failed to generate prompt variants."
        }

    # -----------------------------------------------------
    # STEP 3: Generate Responses
    # -----------------------------------------------------

    responses = {}

    for version, prompt in variants.items():

        response = generate_response(
            prompt
        )

        responses[version] = response

    # -----------------------------------------------------
    # STEP 4: Evaluate Responses
    # -----------------------------------------------------

    evaluation_results = {}

    for version, prompt in variants.items():

        response = responses[version]

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

    # -----------------------------------------------------
    # STEP 5: Select Best Prompt
    # -----------------------------------------------------

    best_version, best_score = select_best_prompt(
        evaluation_results
    )

    best_prompt = variants[
        best_version
    ]

    # -----------------------------------------------------
    # STEP 6: Improve Best Prompt
    # -----------------------------------------------------

    best_evaluation = evaluation_results[
        best_version
    ]["results"]

    final_improved_prompt = improve_best_prompt(
        best_prompt,
        best_evaluation
    )

    # -----------------------------------------------------
    # STEP 7: Return Final Result
    # -----------------------------------------------------

    return {

        "original_prompt": original_prompt,

        "variants": variants,

        "responses": responses,

        "evaluation": evaluation_results,

        "best_prompt": best_prompt,

        "best_version": best_version,

        "best_score": best_score,

        "final_improved_prompt": final_improved_prompt
    }