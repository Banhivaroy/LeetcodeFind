import json

FILE = "../Data/Processed/classified_problems.json"

with open(FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)

print("Number of classified problems:", len(problems))

for problem in problems:
    print(problem["id"], "->", problem["title"])