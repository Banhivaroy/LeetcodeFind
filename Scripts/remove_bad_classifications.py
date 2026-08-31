import json

FILE = "../Data/Processed/classified_problems.json"

REMOVE_IDS = {
    5,    # Longest Palindromic Substring
    14    # Longest Common Prefix
}

with open(FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)

problems = [
    problem
    for problem in problems
    if problem["id"] not in REMOVE_IDS
]

with open(FILE, "w", encoding="utf-8") as f:
    json.dump(
        problems,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Removed old classifications for IDs 5 and 14.")
print("Remaining:", len(problems))