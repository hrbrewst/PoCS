import re
from pathlib import Path

def ACCESSING():
#Paths to files containing novels
	paths = { "pride":"/Users/haleybrewster/Desktop/PoCS_2/pride_prejudice.txt" ,
		 "frank":"/Users/haleybrewster/Desktop/PoCS_2/frankenstein.txt",
		"moby":"/Users/haleybrewster/Desktop/PoCS_2/moby_dick.txt",
		 "les_mis":"/Users/haleybrewster/Desktop/PoCS_2/les_mis.txt"}

	books = {}
# since paths is a tuple (contains two items per token in our case name and path) we use a comma in the for loop to iterate through both.
	for name, path in paths.items():
		with open(path , "r", encoding="utf-8") as f:
			books[name] = f.read()
	return books

TOKEN_RE = re.compile(
	r"""
	\.\.\.                          | # ellipsis
	---                             | # em-dash token if you normalize to ---
	[A-Za-z]+(?:'[A-Za-z]+)?        | # words with optional apostrophe (don't)
	\d+(?:\.\d+)?                   | # integers/decimals
	[^\s]                             # any single non-space char (punctuation)
	""",
	re.VERBOSE
)

def tokenize_1grams(text:str) -> list[str]:
	text =text.replace("—", "---").replace("–", "-")
	text = re.sub(r"--+", "---", text)
	text = text.replace("_", "")
	return TOKEN_RE.findall(text)

def first_paragraph(text: str)-> str:
	text = text.replace("r\n", "\n").replace("\r", "\n").strip()
	return re.split(r"\n\s*\n", text, maxsplit=1)[0]

def save_timeseries(tokens: list[str], out_path: str):
	Path(out_path).write_text("\n".join(tokens) + "\n", encoding="utf-8")

def Q_2():
	books = ACCESSING()
	for name, raw in books.items():
		clean = raw
		tokens = tokenize_1grams(clean)
		out_file = f"/Users/haleybrewster/Desktop/PoCS_2/{name}_narrative_timeseries.txt"
		save_timeseries(tokens, out_file)

        # Report: first paragraph rendered as a single wrapped line
	fp = first_paragraph(clean)
	fp_tokens = tokenize_1grams(fp)
	print(f"\n=== {name} first paragraph as one line ===")
	print(" ".join(fp_tokens))
	print(f"(saved: {out_file}, total tokens: {len(tokens)})")
Q_2()
