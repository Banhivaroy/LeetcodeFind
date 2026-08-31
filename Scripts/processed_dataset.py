import pandas as pd
import json

file_path = "../Data/Raw/leetcode_dataset.xlsx"

df = pd.read_excel(file_path)

selected_columns = [
    "id",
    "title",
    "description",
    "difficulty",
    "url",
    "related_topics",
    "similar_questions"
]

processed_df = df[selected_columns]

processed_df = processed_df.where(pd.notna(processed_df), None)

problems = []

for _, row in processed_df.iterrows():
    problem = row.to_dict()
    problems.append(problem)

output_file = "../Data/Processed/Problems.json"

with open(output_file, "w",encoding="utf-8") as f:
    json.dump(problems, f, ensure_ascii=False, indent=2 )
print(len(problems))
print(problems[0])