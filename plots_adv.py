import pandas as pd
import matplotlib.pyplot as plt

# ====================================================
# LOAD FILES
# ====================================================
full_df = pd.read_csv("combined_fitocracy_general_replies.csv")
vader_df = pd.read_csv("vader_label_proportions.csv")
mean_df = pd.read_csv("mean_lengths_by_group.csv")
nrc_df = pd.read_csv("nrc_summary_by_group.csv")

group_order = ["women_general", "men_general", "women_fitocracy", "men_fitocracy"]
pretty_labels = ["Women General", "Men General", "Women Fitocracy", "Men Fitocracy"]

# ====================================================
# 1. BOX PLOT: COMMENT LENGTH
# ====================================================
plt.figure(figsize=(8, 6))

box_data = [
    full_df.loc[full_df["group"] == g, "n_words"]
    for g in group_order
]

plt.boxplot(box_data, labels=pretty_labels, showfliers=False)
plt.title("Comment Length Distribution by Group")
plt.ylabel("Number of Words")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

# ====================================================
# 2. STACKED BAR CHART: VADER PROPORTIONS
# ====================================================
vader_plot = vader_df.pivot(index="group", columns="vader_label", values="proportion")
vader_plot = vader_plot.reindex(group_order)
vader_plot = vader_plot[["negative", "neutral", "positive"]]
vader_plot.index = pretty_labels

ax = vader_plot.plot(kind="bar", stacked=True, figsize=(8, 6))
plt.title("VADER Sentiment Proportions by Group")
plt.xlabel("")
plt.ylabel("Proportion of Replies")
plt.xticks(rotation=20)
plt.legend(title="Sentiment")
plt.tight_layout()
plt.show()

# ====================================================
# 3. HEATMAP: KEY METRICS
# ====================================================
# fix mean_df if needed
if "group" not in mean_df.columns or "mean_n_words" not in mean_df.columns:
    mean_df.columns = ["group", "mean_n_words"]

# get VADER positive/negative proportions
vader_summary = vader_df.pivot(index="group", columns="vader_label", values="proportion").reset_index()
vader_summary = vader_summary[["group", "positive", "negative"]]
vader_summary = vader_summary.rename(columns={
    "positive": "vader_positive",
    "negative": "vader_negative"
})

# merge files
heat_df = mean_df.merge(vader_summary, on="group").merge(nrc_df, on="group")

# keep selected columns
heat_df = heat_df[[
    "group",
    "mean_n_words",
    "vader_positive",
    "vader_negative",
    "positive_per_word",
    "negative_per_word",
    "joy_per_word",
    "anger_per_word"
]]

# rename NRC columns for cleaner display
heat_df = heat_df.rename(columns={
    "positive_per_word": "nrc_positive",
    "negative_per_word": "nrc_negative",
    "joy_per_word": "nrc_joy",
    "anger_per_word": "nrc_anger"
})

# reorder rows
heat_df["group"] = pd.Categorical(heat_df["group"], categories=group_order, ordered=True)
heat_df = heat_df.sort_values("group")
heat_df = heat_df.set_index("group")
heat_df.index = pretty_labels

# normalize each column 0–1 for display
heat_norm = heat_df.copy()
for col in heat_norm.columns:
    heat_norm[col] = heat_norm[col] / heat_norm[col].max()

plt.figure(figsize=(10, 6))
plt.imshow(heat_norm, aspect="auto")
plt.colorbar(label="Normalized Value")
plt.xticks(range(len(heat_norm.columns)), heat_norm.columns, rotation=45, ha="right")
plt.yticks(range(len(heat_norm.index)), heat_norm.index)
plt.title("Normalized Comparison of Key Metrics by Group")
plt.tight_layout()
plt.show()
