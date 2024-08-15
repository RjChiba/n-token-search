import os, sys
CRR_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(CRR_DIR, "../src/"))
from ja_itaiji import Itaiji

similar = Itaiji.get_similar("満州開拓移民送出分布")
print(len(similar))
print(similar[30:50])