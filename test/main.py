import sys, os
CRR_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(CRR_DIR, "../src/"))
from genindex import generate_nindex
from search import search

if __name__ == "__main__":
	DATA_ID = "text03"
	INDEX_PATH = os.path.join(CRR_DIR, f"./data/index/{DATA_ID}.json")
	DATA_PATH = os.path.join(CRR_DIR, f"./data/raw/{DATA_ID}.txt")

	generate_nindex(INDEX_PATH, DATA_PATH)

	search_text = "dolor in reprehenderit"
	res = search(INDEX_PATH, DATA_PATH, search_text)

	print(*res, sep="\n")