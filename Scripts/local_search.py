import json

CONCEPTS_FILE = "../Data/Processed/Concepts.json"
CLASSIFIED_FILE = "../Data/Processed/classified_problems.json"


# -----------------------------------------
# Load data
# -----------------------------------------

with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
    concepts = json.load(f)

with open(CLASSIFIED_FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)


# -----------------------------------------
# Find concepts from user query
# -----------------------------------------

def find_matching_concepts(query, concepts):

    query = query.lower()

    matches = []

    for concept in concepts:

        searchable_terms = [
            concept["name"],
            *concept["aliases"]
        ]

        for term in searchable_terms:

            if term.lower() in query:

                matches.append(concept)

                break

    return matches


def get_problem_concepts(problem):

    concept_names = set()

    for category in [
        "topics",
        "patterns",
        "techniques",
        "objectives"
    ]:

        for concept in problem[category]:
            concept_names.add(concept["name"])

    return concept_names


def search_problems(query, concepts, problems):

    matched_concepts = find_matching_concepts(
        query,
        concepts
    )

    if not matched_concepts:
        return []

    query_concept_names = {
        concept["name"]
        for concept in matched_concepts
    }

    weights = {
        "topics": 1,
        "patterns": 3,
        "techniques": 2,
        "objectives": 2
    }

    results = []

    for problem in problems:

        score = 0
        matched = []

        for category in weights:

            for concept in problem[category]:

                name = concept["name"]

                if name in query_concept_names:

                    score += weights[category]

                    matched.append({
                        "name": name,
                        "category": category
                    })

        if matched:

            results.append({
                "score": score,
                "title": problem["title"],
                "difficulty": problem["difficulty"],
                "url": problem["url"],
                "matched_concepts": matched
            })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results
# -----------------------------------------
# Test query
# -----------------------------------------

query = "array mirror index"

results = search_problems(
    query,
    concepts,
    problems
)

print("\nUser query:")
print(query)

print("\nSearch results:")

for result in results:

    print(f"\nScore: {result['score']}")
    print(f"Problem: {result['title']}")
    print(f"Difficulty: {result['difficulty']}")

    print("Matched concepts:")

    for concept in result["matched_concepts"]:
        print(
            f"  - {concept['name']} "
            f"({concept['category']})"
        )

    print(f"LeetCode: {result['url']}")