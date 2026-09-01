import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data" / "Processed"

CONCEPTS_FILE = DATA_DIR / "Concepts.json"
EMBEDDINGS_FILE = DATA_DIR / "concept_embeddings.npy"
METADATA_FILE = DATA_DIR / "concept_metadata.json"


# --------------------------------------------------
# Load concepts
# --------------------------------------------------

with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
    concepts = json.load(f)


# --------------------------------------------------
# Build searchable text for each concept
# --------------------------------------------------

def build_concept_text(concept):
    return f"""
Concept: {concept['name']}
Category: {concept['category']}
Description: {concept['description']}
Aliases: {', '.join(concept['aliases'])}
Examples: {', '.join(concept['examples'])}
Related topics: {', '.join(concept['related_topics'])}
Include when: {' '.join(concept['include_when'])}
""".strip()


concept_texts = [
    build_concept_text(concept)
    for concept in concepts
]


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(
     "sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------

print("Creating embeddings...")

embeddings = model.encode_document(
    concept_texts,
    normalize_embeddings=True,
    show_progress_bar=True
)


# --------------------------------------------------
# Save embeddings
# --------------------------------------------------

np.save(
    EMBEDDINGS_FILE,
    embeddings
)


# --------------------------------------------------
# Save concept metadata
# --------------------------------------------------

metadata = []

for concept in concepts:
    metadata.append({
        "name": concept["name"],
        "category": concept["category"],
        "parent": concept["parent"]
    })


with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(
        metadata,
        f,
        ensure_ascii=False,
        indent=2
    )


# --------------------------------------------------
# Print information
# --------------------------------------------------

print("\nEmbedding generation complete.")

print("Number of concepts:", len(concepts))
print("Embedding shape:", embeddings.shape)

print("\nSaved:")
print(EMBEDDINGS_FILE)
print(METADATA_FILE)