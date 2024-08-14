# n-token search engine

full-text engine using n-token method.

## requirements
* python3.9 or older
* install packages from `requirements.txt` 
```shell
pip install -r requirements.txt
```

## usage
1. generate index file
```python
from genindex import generate_nindex

DATA_PATH  = "PATH TO TXT FILE"
INDEX_PATH = "PATH TO INDEX FILE TO SAVE"
generate_nindex(INDEX_PATH, DATA_PATH)
```

2. execute search
```python
from search import search

search_text = "dolor in reprehenderit" # your search words or sentence
res = search(INDEX_PATH, DATA_PATH, search_text)

print(*res, sep="\n")
# > [priority: float, text: str]

# search tokens: [dolor, in]
# [0.5, 'Lorem ipsum dolor sit amet, cons']
# [0.5, 'or in reprehenderit in voluptate velit e']
# [0.5, ' non proident, sunt in culpa qui officia']
# [1.0, 'at. Duis aute irure dolor in reprehender']
```