import os, sys
from ja_itaiji import Itaiji

similar = Itaiji.get_similar("満州開拓移民送出分布")
print(len(similar))
print(similar[30:50])