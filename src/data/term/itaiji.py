import sys, os
import json

CRR_DIR = os.path.dirname(os.path.abspath(__file__))

# load html data
with open(os.path.join(CRR_DIR, "./ja-itaiji.txt"), "r", encoding="utf-8") as f:
	text = f.read()

# convert html to json
# <tr><td>皑</td><td>皑 皚</td></tr>
kv_pairs = text.replace("<tr>", "").split("</tr>") # list of <td>皑</td><td>皑 皚</td>

itaiji = {}
for kv in kv_pairs:
	kv = kv.replace("<td>", "").split("</td>")
	
	if len(kv) < 2:
		continue

	k, v = kv[0], kv[1].split(" ")
	itaiji[k] = v

# save json
with open(os.path.join(CRR_DIR, "./ja-itaiji.json"), "w", encoding="utf-8") as f:
	json.dump(itaiji, f, ensure_ascii=False)