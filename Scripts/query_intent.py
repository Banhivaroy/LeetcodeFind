# -----------------------------------------
# Determine query intent
# -----------------------------------------

def determine_query_intent(
    query,
    query_concepts
):

    intent = {
        "required": [],
        "supporting": []
    }

    if not query_concepts:
        return intent

    query_lower = query.lower()

    # --------------------------------------------------
    # 1. Explicitly mentioned specific patterns
    # --------------------------------------------------

    explicit_patterns = []

    for concept in query_concepts:

        name = concept["name"].lower()

        if (
            concept["category"] == "pattern"
            and name in query_lower
        ):
            explicit_patterns.append(concept)


    # --------------------------------------------------
    # 2. Explicitly mentioned objectives
    # --------------------------------------------------

    explicit_objectives = []

    for concept in query_concepts:

        name = concept["name"].lower()

        if (
            concept["category"] == "objective"
            and name in query_lower
        ):
            explicit_objectives.append(concept)


    # --------------------------------------------------
    # 3. Explicitly mentioned techniques
    # --------------------------------------------------

    explicit_techniques = []

    for concept in query_concepts:

        name = concept["name"].lower()

        if (
            concept["category"] == "technique"
            and name in query_lower
        ):
            explicit_techniques.append(concept)


    # --------------------------------------------------
    # Choose required concepts
    # --------------------------------------------------

    if explicit_patterns:

        intent["required"].extend(
            explicit_patterns
        )

    elif explicit_objectives:

        intent["required"].extend(
            explicit_objectives
        )

    elif explicit_techniques:

        intent["required"].extend(
            explicit_techniques
        )

    else:

        # Nothing explicit.
        # Use strongest semantic concept.
        strongest = max(
            query_concepts,
            key=lambda x: x.get("score", 0)
        )

        intent["required"].append(
            strongest
        )


    # --------------------------------------------------
    # Everything else becomes supporting
    # --------------------------------------------------

    required_names = {
        concept["name"]
        for concept in intent["required"]
    }

    for concept in query_concepts:

        if concept["name"] not in required_names:

            intent["supporting"].append(
                concept
            )


    return intent

#  ------------------------------------------------------------------
if __name__ == "__main__":

    query_concepts = [
        {
            "name": "mirror index",
            "category": "pattern",
            "score": 0.7431
        },
        {
            "name": "array",
            "category": "topic",
            "score": 0.5277
        },
        {
            "name": "two indices",
            "category": "pattern",
            "score": 0.4301
        }
    ]

    query = "array mirror index"

    intent = determine_query_intent(
        query,
        query_concepts
    )

    print("\nRequired:")

    for concept in intent["required"]:
        print("-", concept["name"])

    print("\nSupporting:")

    for concept in intent["supporting"]:
        print("-", concept["name"])