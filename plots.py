import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ====================================================
# LOAD FILES
# ====================================================
mean_df = pd.read_csv("mean_lengths_by_group.csv")
vader_df = pd.read_csv("vader_label_proportions.csv")
nrc_df = pd.read_csv("nrc_summary_by_group.csv")

# ====================================================
# CLEAN / STANDARDIZE
# ====================================================

# Mean lengths file sometimes saves with unnamed first column
if "group" not in mean_df.columns or "mean_n_words" not in mean_df.columns:
    mean_df.columns = ["group", "mean_n_words"]

group_order = ["women_general", "men_general", "women_fitocracy", "men_fitocracy"]

# ====================================================
# 1. MEAN COMMENT LENGTH BAR CHART
# ====================================================
mean_plot = mean_df.copy()
mean_plot["group"] = pd.Categorical(mean_plot["group"], categories=group_order, ordered=True)
mean_plot = mean_plot.sort_values("group")

plt.figure(figsize=(8,6))
plt.bar(mean_plot["group"], mean_plot["mean_n_words"])
plt.title("Mean Comment Length by Group")
plt.xlabel("Group")
plt.ylabel("Mean Number of Words")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ====================================================
# 2. VADER STACKED BAR CHART
# ====================================================
vader_plot = vader_df.pivot(index="group", columns="vader_label", values="proportion")

# reorder rows and columns
vader_plot = vader_plot.reindex(group_order)
vader_plot = vader_plot[["negative", "neutral", "positive"]]

ax = vader_plot.plot(
    kind="bar",
    stacked=True,
    figsize=(8,6)
)

plt.title("VADER Sentiment Proportions by Group")
plt.xlabel("Group")
plt.ylabel("Percent of Replies")
plt.xticks(rotation=45)
plt.legend(title="Sentiment")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.tight_layout()
plt.show()

# ====================================================
# 3. NRC BAR CHART
#    Pick a few categories that are easiest to explain
# ====================================================
nrc_plot = nrc_df.copy()
nrc_plot["group"] = pd.Categorical(nrc_plot["group"], categories=group_order, ordered=True)
nrc_plot = nrc_plot.sort_values("group")

selected_cols = [
    "positive_per_word",
    "negative_per_word",
    "joy_per_word",
    "anger_per_word"
]

nrc_plot = nrc_plot.set_index("group")[selected_cols]

ax = nrc_plot.plot(
    kind="bar",
    figsize=(10,6)
)

plt.title("Selected NRC Emotion Rates by Group")
plt.xlabel("Group")
plt.ylabel("Rate per Word")
plt.xticks(rotation=45)
plt.legend(title="NRC Category")
plt.tight_layout()
plt.show()
