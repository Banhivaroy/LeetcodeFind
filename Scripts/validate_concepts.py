import json

CONCEPTS_FILE = "../Data/Processed/Concepts.json"

with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
    concepts = json.load(f)


# --------------------------------------------------
# 1. Check required fields
# --------------------------------------------------

required_fields = [
    "name",
    "parent",
    "category",
    "description",
    "aliases",
    "examples",
    "related_topics",
    "include_when"
]

for concept in concepts:
    for field in required_fields:
        if field not in concept:
            print(
                f"Missing '{field}' in concept: "
                f"{concept.get('name', '<unknown>')}"
            )


# --------------------------------------------------
# 2. Check duplicate names
# --------------------------------------------------

names = [concept["name"] for concept in concepts]

duplicates = {
    name
    for name in names
    if names.count(name) > 1
}

if duplicates:
    print("\nDuplicate concept names:")
    for name in duplicates:
        print("-", name)
else:
    print("\nNo duplicate concept names.")


# --------------------------------------------------
# 3. Create a set for fast lookup
# --------------------------------------------------

concept_names = set(names)


# --------------------------------------------------
# 4. Check parent references
# --------------------------------------------------

for concept in concepts:

    parent = concept["parent"]

    if parent is not None and parent not in concept_names:
        print(
            f"\nInvalid parent in '{concept['name']}': "
            f"'{parent}'"
        )


# --------------------------------------------------
# 5. Check related topic references
# --------------------------------------------------

for concept in concepts:

    for related in concept["related_topics"]:

        if related not in concept_names:
            print(
                f"\nInvalid related topic in "
                f"'{concept['name']}': '{related}'"
            )


print("\nNumber of concepts:", len(concepts))
print("Validation finished.")