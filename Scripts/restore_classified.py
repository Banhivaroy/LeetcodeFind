import json


PROBLEMS_FILE = "../Data/Processed/Problems.json"
OUTPUT_FILE = "../Data/Processed/classified_problems.json"


# --------------------------------------------------
# Load original problems
# --------------------------------------------------

with open(PROBLEMS_FILE, "r", encoding="utf-8") as f:
    problems = json.load(f)


# --------------------------------------------------
# Load existing classifications
# --------------------------------------------------

try:
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        classified_problems = json.load(f)

except FileNotFoundError:
    classified_problems = []


# --------------------------------------------------
# Existing IDs
# --------------------------------------------------

existing_ids = {
    problem["id"]
    for problem in classified_problems
}


# --------------------------------------------------
# Classifications already obtained from Gemini
# --------------------------------------------------

known_classifications = {

    "Two Sum": {
        "topics": ["array"],
        "patterns": [
            "two indices",
            "complement lookup"
        ],
        "techniques": [
            "hashing"
        ],
        "objectives": []
    },

    "3Sum": {
        "topics": ["array"],
        "patterns": [
            "three indices",
            "three sum",
            "two indices",
            "duplicate detection",
            "sorted array"
        ],
        "techniques": [
            "sorting",
            "two pointers"
        ],
        "objectives": []
    },

    "Merge Intervals": {
        "topics": ["array"],
        "patterns": [
            "interval",
            "merge intervals",
            "sorted array"
        ],
        "techniques": [
            "greedy",
            "sorting"
        ],
        "objectives": []
    },

    "Binary Tree Level Order Traversal": {
        "topics": [
            "tree",
            "queue",
            "binary tree"
        ],
        "patterns": [],
        "techniques": [
            "breadth first search",
            "tree traversal"
        ],
        "objectives": []
    },

    "Valid Palindrome": {
        "topics": ["string"],
        "patterns": [
            "palindrome",
            "mirror index",
            "symmetry"
        ],
        "techniques": [
            "two pointers"
        ],
        "objectives": []
    },

    "House Robber": {
        "topics": ["array"],
        "patterns": [
            "adjacent indices",
            "take or skip",
            "one dimensional dp",
            "subsequence"
        ],
        "techniques": [
            "dynamic programming",
            "state transition"
        ],
        "objectives": [
            "maximize value"
        ]
    },

    "Longest Increasing Subsequence": {
        "topics": ["array"],
        "patterns": [
            "subsequence",
            "state transition",
            "one dimensional dp",
            "subsequence dp",
            "increasing subsequence"
        ],
        "techniques": [
            "dynamic programming",
            "binary search"
        ],
        "objectives": [
            "maximize value"
        ]
    }
}


# --------------------------------------------------
# Restore missing classifications
# --------------------------------------------------

for problem in problems:

    title = problem["title"]

    if title not in known_classifications:
        continue

    if problem["id"] in existing_ids:
        print(
            f"Already exists: {title}"
        )
        continue

    classification = known_classifications[title]

    classified_problem = {
        "id": problem["id"],
        "title": problem["title"],
        "description": problem["description"],
        "difficulty": problem["difficulty"],
        "url": problem["url"],
        "topics": [
            {
                "name": name,
                "confidence": 1.0,
                "reason": "Restored from previous classification."
            }
            for name in classification["topics"]
        ],
        "patterns": [
            {
                "name": name,
                "confidence": 1.0,
                "reason": "Restored from previous classification."
            }
            for name in classification["patterns"]
        ],
        "techniques": [
            {
                "name": name,
                "confidence": 1.0,
                "reason": "Restored from previous classification."
            }
            for name in classification["techniques"]
        ],
        "objectives": [
            {
                "name": name,
                "confidence": 1.0,
                "reason": "Restored from previous classification."
            }
            for name in classification["objectives"]
        ]
    }

    classified_problems.append(
        classified_problem
    )

    print(
        f"Restored: {title}"
    )


# --------------------------------------------------
# Save
# --------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        classified_problems,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    f"\nTotal classified problems: "
    f"{len(classified_problems)}"
)