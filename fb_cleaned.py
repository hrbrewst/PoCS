import pandas as pd
import re

# IMPORTING FILE ------------------------------

file_path = "/Users/haleybrewster/Desktop/PoCS_2/project_data/facebook_wiki_responses.csv"
output_path = "/Users/haleybrewster/Desktop/PoCS_2/pd_cleaned/fb_responses_clean.csv"

df = pd.read_csv(file_path)


# CLEANING ---------------------------------
# column names: lowercase and no spaces

df.columns = [col.strip().lower() for col in df.columns]

# Rename possible variants into one consistent naming scheme
rename_map = {
    "op_gender": "gender",
    "reply_text": "text",
    "response_text": "text",
    "comment_text": "text",
    "sentiment_annotation": "sentiment",
    "reply_sentiment": "sentiment",
    "thread-type": "thread_type",
    "thread type": "thread_type"
}

df = df.rename(columns=rename_map)


#  KEEP ONLY USEFUL COLUMNS ------------------------

wanted_cols = [
    "op_id", "gender","post_id","text","sentiment",
    "thread_type","post_type", "platform"
]

existing_cols = [col for col in wanted_cols if col in df.columns]
df = df[existing_cols].copy()



# CLEAN GENDER LABELS -------------------

def clean_gender(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().lower()

    if x in ["f", "female", "woman", "women"]:
        return "female"
    elif x in ["m", "male", "man", "men"]:
        return "male"
    else:
        return pd.NA

if "gender" in df.columns:
    df["gender"] = df["gender"].apply(clean_gender)


# ---------------------------------
# 5. CLEAN THREAD TYPE
# ---------------------------------
def clean_thread_type(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().lower()

    if x in ["sports", "sport"]:
        return "sports"
    elif x in ["general", "baseline", "non-sports", "nonsports", "non sports"]:
        return "general"
    else:
        return pd.NA

if "thread_type" in df.columns:
    df["thread_type"] = df["thread_type"].apply(clean_thread_type)


# ---------------------------------
# 6. CLEAN SENTIMENT LABELS
# ---------------------------------
def clean_sentiment(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().lower()

    if x in ["positive", "pos"]:
        return "positive"
    elif x in ["neutral", "neu"]:
        return "neutral"
    elif x in ["negative", "neg"]:
        return "negative"
    elif x in ["mixed", "mix"]:
        return "mixed"
    else:
        return pd.NA

if "sentiment" in df.columns:
    df["sentiment"] = df["sentiment"].apply(clean_sentiment)


# ---------------------------------
# 7. CLEAN REPLY TEXT
# ---------------------------------
def clean_text(text):
    if pd.isna(text):
        return pd.NA

    text = str(text)

    # remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove @mentions
    text = re.sub(r"@\w+", "", text)

    # remove HTML entities like &amp;
    text = re.sub(r"&\w+;", " ", text)

    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text if text != "" else pd.NA

if "text" in df.columns:
    df["text"] = df["text"].apply(clean_text)


# ---------------------------------
# 8. DROP MISSING / BAD ROWS
# ---------------------------------
required_cols = [col for col in ["gender", "text", "thread_type"] if col in df.columns]
df = df.dropna(subset=required_cols)

print("\nShape after dropping missing required values:", df.shape)


# ---------------------------------
# 9. REMOVE DUPLICATES
# ---------------------------------
dup_cols = [col for col in ["post_id", "text"] if col in df.columns]

if len(dup_cols) > 0:
    df = df.drop_duplicates(subset=dup_cols)

print("Shape after dropping duplicates:", df.shape)


# ---------------------------------
# 10. ADD WORD COUNT
# ---------------------------------
if "text" in df.columns:
    df["n_words"] = df["text"].str.split().str.len()


# ---------------------------------
# 11. OPTIONAL: ADD PLATFORM NAME IF MISSING
# ---------------------------------
if "platform" not in df.columns:
    df["platform"] = "unknown"


# ---------------------------------
# 12. REORDER COLUMNS
# ---------------------------------
final_order = [
    "platform",
    "op_id",
    "post_id",
    "gender",
    "thread_type",
    "sentiment",
    "post_type",
    "text",
    "n_words"
]

final_cols = [col for col in final_order if col in df.columns]
df = df[final_cols].copy()

#Saving file
df.to_csv(output_path, index=False)

