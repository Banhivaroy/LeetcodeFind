import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

# --------------------------------------------------
# File paths
# --------------------------------------------------

PROBLEMS_FILE = "../Data/Processed/Problems.json"
CONCEPTS_FILE = "../Data/Processed/Concepts.json"


OUTPUT_FILE = "../Data/Processed/classified_problems.json"

try:
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        classified_problems = json.load(f)

except FileNotFoundError:
    classified_problems = []

processed_ids = {
    problem["id"]
    for problem in classified_problems
}
# --------------------------------------------------
# Load datasets
# --------------------------------------------------

with open(PROBLEMS_FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)
    

with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
    concepts = json.load(f)  

# --------------------------------------------------
# Load Gemini API key
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Convert concepts into text for Gemini
# --------------------------------------------------

def build_concept_text(concepts):
    lines = []

    for concept in concepts:
        lines.append(
            f"""
Concept: {concept['name']}
Category: {concept['category']}
Description: {concept['description']}
Aliases: {', '.join(concept['aliases'])}
Examples: {', '.join(concept['examples'])}
Related topics: {', '.join(concept['related_topics'])}
Include when: {' '.join(concept['include_when'])}
""".strip()
        )

    return "\n\n".join(lines)


# --------------------------------------------------
# Convert one problem into text
# --------------------------------------------------

def build_problem_text(problem):
    return f"""
Title: {problem['title']}

Description:
{problem['description']}

Existing topics:
{problem['related_topics']}
""".strip()

# --------------------------------------------------
# Use the complete problem dataset
# --------------------------------------------------

problems_to_classify = problems

print("Total problems:", len(problems_to_classify))
print("Already classified:", len(classified_problems))

print(
    "Remaining:",
    len(problems_to_classify) - len(processed_ids)
)


# --------------------------------------------------
# Build the prompt
# --------------------------------------------------

# --------------------------------------------------
# Classify one problem
# --------------------------------------------------

def classify_problem(problem, concept_text):

    problem_text = build_problem_text(problem)

    classifier_prompt = f"""
You are an expert Data Structures and Algorithms problem classifier.

Your task is to identify which concepts from the provided controlled
vocabulary apply to the given programming problem.

RULES:

1. Only use concepts from the provided vocabulary.
2. Never invent a new concept.
3. Assign a concept only when its "include_when" conditions are satisfied.
4. Consider the underlying algorithmic structure, not just words appearing
   in the problem statement.
5. A problem can have multiple applicable concepts.
6. Do not assign a technique merely because it could theoretically solve
   the problem.
7. Prefer specific concepts when they clearly apply.
8. Give a short reason for every selected concept.
9. Do not include markdown code fences.
10. Do not include any text before or after the JSON.
11. Do not assign a concept merely because it is a general property
    of a technique used in the solution.
12. Do not assign a parent concept when a more specific child concept
    captures the same idea, unless the parent is independently useful
    as a classification.
13. Do not assign generic concepts such as "state transition",
    "optimization objective", or "maximize value" merely because
    they technically describe the solution.
14. A concept must represent a meaningful searchable characteristic
    of the problem or its primary solution approach.
15. Prefer the most specific concept available in the vocabulary.
16. "Related topics" must not be treated as evidence that a concept
    applies.
17. For a concept to be assigned, its "include_when" conditions must
    be directly satisfied by the problem or its canonical solution,
    not merely indirectly implied.
18. When uncertain, omit the concept rather than assigning it.
19. Classify concepts based on their usefulness as searchable
    characteristics of the problem.
20. Do not assign a concept merely because it is a mathematical
    consequence, generic property, or low-level implementation detail
    of another selected concept.
21. Generic concepts should only be selected when they provide
    meaningful search value beyond a more specific concept.
22. For example, if a problem is specifically "Longest Common
    Subsequence", do not automatically assign generic concepts such
    as "maximize value" simply because "longest" implies maximization.
23. Do not assign "take or skip" merely because a DP recurrence chooses
    between two states. The include/exclude decision must itself be a
    central and reusable problem pattern.

24. Do not assign "subsequence" merely because elements can be skipped.
    The selected elements must themselves form the central sequence,
    constraint, or output of the problem.

25. Do not assign "take or skip" merely because a DP recurrence has
    multiple alternatives. The take/skip decision must be a central,
    reusable problem pattern.

26. Do not assign "state transition" merely because the solution uses
    a DP recurrence. Only select it when the transition structure itself
    is a meaningful searchable characteristic.

27. Do not assign "recursion" merely because a DP solution can be written
    using recursive memoization. Recursion must be central to the intended
    solution.

28. Prefer specific objective concepts such as "minimize count",
    "maximize value", or "maximize length" over generic
    "optimization objective".

29. Do not assign "maximize count" when the problem asks for maximum
    length, maximum value, or another non-count quantity.

30. Do not assign generic concepts merely because they are technically
    present in the implementation. Every selected concept must provide
    meaningful search value.

31. Prefer the most specific concept available when it captures the same
    idea more precisely.

32. "Related topics" must not be treated as evidence that a concept applies.

33. For Longest Common Subsequence, prefer specific concepts such as
    "longest common subsequence", "subsequence of string",
    "two dimensional dp", "subsequence dp", and "dynamic programming"
    when their conditions are satisfied.

34. For LCS, do not automatically assign generic concepts such as
    "two indices", "take or skip", or "state transition" merely because
    they appear in the recurrence. 

PROBLEM:
{problem_text}

CONTROLLED CONCEPT VOCABULARY:
{concept_text}

Return ONLY valid JSON.

Each item in every category MUST contain exactly these fields:

- "name"
- "confidence"
- "reason"

The "name" field MUST exactly match a concept name from the
controlled vocabulary.

Use this exact structure:

{{
  "topics": [
    {{
      "name": "string",
      "confidence": 1.0,
      "reason": "The problem operates on strings."
    }}
  ],
  "patterns": [
    {{
      "name": "longest common subsequence",
      "confidence": 1.0,
      "reason": "The problem directly asks for the longest common subsequence."
    }}
  ],
  "techniques": [
    {{
      "name": "dynamic programming",
      "confidence": 1.0,
      "reason": "The canonical solution uses overlapping subproblems."
    }}
  ],
  "objectives": []
}}

IMPORTANT:
- Never use "concept" as a field name.
- Always use "name".
- "name" must exactly match one of the concept names in the vocabulary.
- "confidence" must be a number between 0 and 1.
- "reason" must briefly explain why the concept applies.
- Use [] when no concepts from a category apply.
- Do not include markdown code fences.
- Do not include any text before or after the JSON.
""".strip()

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=classifier_prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )
            break

        except errors.ServerError:

            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    result = json.loads(response.text)

    valid_concept_names = {
        concept["name"]
        for concept in concepts
    }

    categories = [
        "topics",
        "patterns",
        "techniques",
        "objectives"
    ]

    for category in categories:

        for concept in result[category]:

            name = concept["name"]

            if name not in valid_concept_names:
                print(
                    f"WARNING: Unknown concept '{name}' "
                    f"in category '{category}'"
                )

    return result


concept_text = build_concept_text(concepts)



for problem in problems_to_classify:

    if problem["id"] in processed_ids:
        print(f"Skipping already classified: {problem['title']}")
        continue


    print("\n" + "=" * 60)
    print("PROBLEM:", problem["title"])
    print("=" * 60)

    try:
        result = classify_problem(problem, concept_text)

        classified_problem = {
            "id": problem["id"],
            "title": problem["title"],
            "description": problem["description"],
            "difficulty": problem["difficulty"],
            "url": problem["url"],
            "topics": result["topics"],
            "patterns": result["patterns"],
            "techniques": result["techniques"],
            "objectives": result["objectives"]
        }

        classified_problems.append(classified_problem)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(
            classified_problems,
            f,
            ensure_ascii=False,
            indent=2
        )
        processed_ids.add(problem["id"])

        print("Saved:", problem["title"])

        for category in [
            "topics",
            "patterns",
            "techniques",
            "objectives"
        ]:

            print(f"\n{category.upper()}:")

            for concept in result[category]:
                print(f"- {concept['name']}")

    except errors.APIError as e:

        if e.code == 429:
            print("\nGemini quota exhausted.")
            print("Stopping batch so existing results are preserved.")
            break

        print("\nCLASSIFICATION FAILED:")
        print(e)


    except Exception as e:

        print("\nCLASSIFICATION FAILED:")
        print(e)


    time.sleep(1)

print(
    f"\nSaved {len(classified_problems)} "
    f"classified problems."
)