import pandas as pd
import os

# -------------------------------------------------
# 1. PUT YOUR FILE NAMES HERE
# -------------------------------------------------
# Change these to your actual file names
files_and_mappings = [
    {
        "file": "facebook_wiki_posts.csv",
        "type": "posts",
        "columns": {
            "op_id": "op_id",
            "op_gender": "gender",
            "post_id": "post_id",
            "post_text": "text",
            "post_type": "context"
        }
    },
    {
        "file": "facebook_wiki_responses.csv",
        "type": "replies",
        "columns": {
            "op_id": "op_id",
            "op_gender": "gender",
            "post_id": "post_id",
            "response_text": "text"
            # add sentiment/context here if they exist in this file
            # example: "sentiment": "sentiment",
            # example: "thread_type": "context"
        }
    },

    {
        "file": "fitocracy_posts.csv",
        "type": "posts",
        "columns": {
            "author_gender": "op_gender",
            "id": "op_id",
            "body": "post_text",
        }
    },

    {
        "file": "fitocracy_responses.csv",
        "type": "responses",
        "columns": {
            "author_gender": "op_gender",
            "responder_gender": "responder_gender",
            "id": "post_id",
            "body": "response_text",
        }
    },

    {
        "file": "reddit_posts.csv",
        "type": "posts",
        "columns": {
            "author_gender": "op_gender",
            "id": "post_id",
            "body": "post_text",
        }
    },

    {
        "file": "reddit_responses.csv",
        "type": "responses",
        "columns": {
            "author_gender": "op_gender",   
            "responder_gender": "responder_gender",
            "id": "post_id",
            "body": "response_text",
        }
    },

    {
        "file": "ted_responses.csv",
        "type": "responses",
        "columns": {
            "author_gender": "op_gender",   
            "responder_gender": "responder_gender",
            "id": "post_id",
            "body": "response_text"
        }
    }
]

# -------------------------------------------------
# 2. FOLDER PATH
# -------------------------------------------------
folder_path = "path/to/your/csv_folder"   # change this

# -------------------------------------------------
# 3. LOAD EACH FILE SEPARATELY AND RENAME COLUMNS
# -------------------------------------------------
all_dfs = []

for item in files_and_mappings:
    file_name = item["file"]
    file_type = item["type"]
    col_map = item["columns"]

    file_path = os.path.join(folder_path, file_name)

    print(f"\nReading: {file_name}")

    df = pd.read_csv(file_path)
    print("Original columns:", list(df.columns))

    # keep only columns that exist
    existing_map = {old: new for old, new in col_map.items() if old in df.columns}

    if len(existing_map) == 0:
        print(f"Skipped {file_name}: none of the mapped columns were found.")
        continue

    df = df[list(existing_map.keys())].copy()
    df = df.rename(columns=existing_map)

    df["source_file"] = file_name
    df["file_type"] = file_type

    all_dfs.append(df)

    print("Renamed columns:", list(df.columns))
    print(df.head())

# -------------------------------------------------
# 4. COMBINE EVERYTHING
# -------------------------------------------------
combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)

print("\nCombined shape:", combined_df.shape)
print("\nCombined columns:", list(combined_df.columns))
print(combined_df.head())

combined_df.to_csv("combined_standardized.csv", index=False)
print("\nSaved as combined_standardized.csv")
