import json

conscepts_file = "../Data/Processed/Concepts.json"

with open(conscepts_file,"r",encoding="utf-8") as f:
    concepts = json.load(f)

print("no. of concepts: ",len(concepts))

required_fields = [
    "name",
    "parent",
    "category",
    "description",
    "aliases",
    "examples",
    "related_topics"
]

for concept in concepts:
    for field in required_fields:
        if field not in concept:
            print(
                f"Missing '{field}' in concept: "
                f"{concept.get('name')}"
            )



print("\nFirst concept:")
print(concepts[0])