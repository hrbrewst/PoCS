import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

labmt = pd.read_csv("/Users/haleybrewster/Desktop/PoCS_2/Hedonometer.csv")

# clean column names
labmt.columns = labmt.columns.str.strip().str.lower()

print(labmt.columns.tolist())  # now check

word2score = dict(zip(labmt["word"].str.lower(), labmt["happiness score"]))

pp_path = "/Users/haleybrewster/Desktop/PoCS_2/pride_narrative_timeseries.txt"
with open(pp_path, "r", encoding="utf-8") as f:
    tokens = [line.strip().lower() for line in f if line.strip()]

N = len(tokens)

def emotional_arc(tokens, T, word2score):
    scores = np.array([word2score.get(tok, np.nan) for tok in tokens], dtype=float)
    mask = ~np.isnan(scores)

    s = np.where(mask, scores, 0.0)
    csum = np.concatenate(([0.0], np.cumsum(s)))
    ccount = np.concatenate(([0], np.cumsum(mask.astype(int))))

    wsum = csum[T:] - csum[:-T]
    wcount = ccount[T:] - ccount[:-T]

    avg = wsum / wcount
    avg[wcount == 0] = np.nan  # if a window has zero labMT words

    centers = (np.arange(len(avg)) + T/2) / N * 100.0
    return centers, avg, wcount

mus = [1, 1.5, 2, 2.5, 3, 3.5, 4.0]
Ts = [int(round(10**mu)) for mu in mus]

fig, axes = plt.subplots(len(Ts), 1, figsize=(10, 12), sharex=True)
fig.suptitle(f"Emotional arc (labMT full lens, δh_avg=0)\n{pp_path}", y=0.995)

for ax, mu, T in zip(axes, mus, Ts):
    if T >= N:
        ax.text(0.5, 0.5, f"T={T} is bigger than book length N={N}", ha="center")
        ax.set_axis_off()
        continue

    x, y, wcount = emotional_arc(tokens, T, word2score)

    # optional: downsample if huge (keeps plot fast)
    if len(y) > 6000:
        idx = np.linspace(0, len(y)-1, 6000).astype(int)
        x_plot, y_plot = x[idx], y[idx]
    else:
        x_plot, y_plot = x, y

    ax.plot(x_plot, y_plot, linewidth=1)
    ax.set_ylabel(f"T≈10^{mu}\n(T={T})", rotation=0, labelpad=35, va="center")
    ax.grid(True, alpha=0.3)

    coverage = np.nanmedian(wcount / T)
    ax.text(0.99, 0.85, f"median coverage≈{coverage:.2f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8)

axes[-1].set_xlabel("% of book (window center)")
plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.show()

