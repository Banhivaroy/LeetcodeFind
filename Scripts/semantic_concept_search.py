import json
import numpy as np
from Scripts.concept_to_problem_search import search_problems_by_concepts
from sentence_transformers import SentenceTransformer
from Scripts.query_intent import determine_query_intent


from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data" / "Processed"

CONCEPTS_FILE = DATA_DIR / "concepts.json"
EMBEDDINGS_FILE = DATA_DIR / "concept_embeddings.npy"
METADATA_FILE = DATA_DIR / "concept_metadata.json"
CLASSIFIED_FILE = DATA_DIR / "classified_problems.json"


# -----------------------------------------
# Load concepts
# -----------------------------------------

with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
    concepts = json.load(f)

embeddings = np.load(EMBEDDINGS_FILE)

with open(CLASSIFIED_FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)


# -----------------------------------------
# Load model
# -----------------------------------------

model = SentenceTransformer(
    "sentence-transformers/multi-qa-mpnet-base-cos-v1"
)


# -----------------------------------------
# Semantic search
# -----------------------------------------

def semantic_search(query, top_k=10):

    query_embedding = model.encode_query(
        query,
        normalize_embeddings=True
    )

    similarities = embeddings @ query_embedding

    results = []

    query_lower = query.lower()

    category_weights = {
        "pattern": 1.20,
        "structural": 1.10,
        "technique": 0.90,
        "topic": 0.80,
        "objective": 0.90
    }

    for index, similarity in enumerate(similarities):

        concept = concepts[index]

        score = float(similarity)

        category = concept["category"]

        score *= category_weights.get(
            category,
            1.0
        )

        # Exact concept name
        if concept["name"].lower() in query_lower:
            score += 0.30

        # Alias matching
        for alias in concept["aliases"]:

            if alias.lower() in query_lower:
                score += 0.25
                break

        # Example matching
        for example in concept["examples"]:

            if example.lower() in query_lower:
                score += 0.20
                break

        results.append({
            "name": concept["name"],
            "category": category,
            "score": score,
            "semantic_score": float(similarity)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]

# -----------------------------------
def get_query_concepts(
    query,
    top_k=5,
    minimum_score=0.35,
    relative_threshold=0.75
):

    results = semantic_search(
        query,
        top_k=top_k
    )

    if not results:
        return []

    query_lower = query.lower()

    strongest_score = results[0]["score"]

    query_concepts = []

    for result in results:

        name = result["name"].lower()
        score = result["score"]

        # -----------------------------------------
        # Explicit concept-name match
        # -----------------------------------------

        explicit_match = name in query_lower

        # -----------------------------------------
        # Explicit alias match
        # -----------------------------------------

        alias_match = False

        for concept in concepts:

            if concept["name"].lower() == name:

                for alias in concept["aliases"]:

                    if alias.lower() in query_lower:

                        alias_match = True
                        break

                break

        # -----------------------------------------
        # Decide whether to keep concept
        # -----------------------------------------

        if explicit_match or alias_match:

            query_concepts.append({
                "name": result["name"],
                "category": result["category"],
                "score": score
            })

        elif (
            score >= minimum_score
            and score >= strongest_score * relative_threshold
        ):

            query_concepts.append({
                "name": result["name"],
                "category": result["category"],
                "score": score
            })

    return query_concepts
# -----------------------------------------
#   search from query
# -----------------------------------------
def search_from_query(query):

    query_concepts = get_query_concepts(
        query,
        top_k=5
    )

    intent = determine_query_intent(
        query,
        query_concepts
    )

    print("\nRequired concepts:")

    for concept in intent["required"]:
        print(
            f"- {concept['name']} "
            f"({concept['category']})"
        )

    print("\nSupporting concepts:")

    for concept in intent["supporting"]:
        print(
            f"- {concept['name']} "
            f"({concept['category']})"
        )

    results = search_problems_by_concepts(
        intent,
        problems
    )

    return {
        "required_concepts": [
            concept["name"]
            for concept in intent["required"]
        ],
        "supporting_concepts": [
            concept["name"]
            for concept in intent["supporting"]
        ],
        "results": results
    }
# -----------------------------------------
# Test multiple queries
# -----------------------------------------
if __name__ == "__main__" :
    queries = [
        "array mirror index",
        "subsequence dynamic programming problems",
        "take or skip DP problems",
        "problems using monotonic stack",
        "minimum number of coins dynamic programming",
        "two pointer array problems",
        "problems involving next greater element"
    ]
    

    for query in queries:

        print("\n" + "=" * 60)
        print("QUERY:", query)
        print("=" * 60)

    results = search_from_query(query)

    print("\nMatching LeetCode problems:")

    for result in results[:5]:

        print(
            f"\nScore: {result['score']:.2f}"
        )

        print(
            f"Problem: {result['title']}"
        )

        print(
            f"Difficulty: {result['difficulty']}"
        )

        print(
            f"LeetCode: {result['url']}"
        )

        print("Matched concepts:")

        for concept in result["matched_concepts"]:

            print(
                f"  - {concept['name']} "
                f"({concept['category']})"
            )