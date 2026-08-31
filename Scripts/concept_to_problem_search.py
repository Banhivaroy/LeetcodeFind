import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data" / "Processed"

CONCEPTS_FILE = DATA_DIR / "concepts.json"
CLASSIFIED_FILE = DATA_DIR / "classified_problems.json"


# -----------------------------------------
# Load data
# -----------------------------------------

with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
    concepts = json.load(f)

with open(CLASSIFIED_FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)


# -----------------------------------------
# Get all concepts for a problem
# -----------------------------------------

def get_problem_concepts(problem):

    result = []

    for category in [
        "topics",
        "patterns",
        "techniques",
        "objectives"
    ]:

        for concept in problem[category]:

            result.append({
                "name": concept["name"],
                "category": category
            })

    return result


# -----------------------------------------
# Search problems using query intent
# -----------------------------------------

def search_problems_by_concepts(intent, problems):

    required_concepts = intent["required"]
    supporting_concepts = intent["supporting"]

    required_names = {
        concept["name"]
        for concept in required_concepts
    }

    supporting_names = {
        concept["name"]
        for concept in supporting_concepts
    }

    results = []

    for problem in problems:

        problem_concepts = get_problem_concepts(problem)

        problem_names = {
            concept["name"]
            for concept in problem_concepts
        }

        # Required concepts must exist
        if not required_names.issubset(problem_names):
            continue

        score = 0
        matched = []

        # Required
        for concept in problem_concepts:

            if concept["name"] in required_names:

                query_concept = next(
                    q
                    for q in required_concepts
                    if q["name"] == concept["name"]
                )

                semantic_score = query_concept.get(
                    "score",
                    1.0
                )

                score += 5 * semantic_score

                matched.append(concept)

        # Supporting
        for concept in problem_concepts:

            if concept["name"] in supporting_names:

                query_concept = next(
                    q
                    for q in supporting_concepts
                    if q["name"] == concept["name"]
                )

                semantic_score = query_concept.get(
                    "score",
                    1.0
                )

                score += 1 * semantic_score

                matched.append(concept)

        if matched:

            results.append({
                "score": score,
                "title": problem["title"],
                "difficulty": problem["difficulty"],
                "url": problem["url"],
                "matched_concepts": matched
            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results
# -----------------------------------------
# Manual test
# -----------------------------------------

if __name__ == "__main__":

    test_intent = {

        "required": [
            {
                "name": "mirror index",
                "category": "pattern",
                "score": 1.0
            }
        ],

        "supporting": [
            {
                "name": "array",
                "category": "topic",
                "score": 1.0
            }
        ]
    }


    results = search_problems_by_concepts(
        test_intent,
        problems
    )


    print("\nSearch results:")

    for result in results:

        print(
            "\nScore:",
            result["score"]
        )

        print(
            "Problem:",
            result["title"]
        )

        print(
            "Difficulty:",
            result["difficulty"]
        )

        print(
            "URL:",
            result["url"]
        )

        print("Matched concepts:")

        for concept in result["matched_concepts"]:

            print(
                f"  - {concept['name']} "
                f"({concept['category']})"
            )