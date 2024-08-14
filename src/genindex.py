import os, sys
import json

import spacy

CRR_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_tokens(sent):
	#固有名詞、一般名詞、動詞、形容詞のみ抽出
	pos_tags = ('PROPN', 'NOUN', 'VERB', 'ADJ')
	#不要語
	stopwords = ('する', 'ある', 'ない', 'いう', 'もの', 'こと', 'よう', 'なる', 'ほう', 'いる', 'くる')

	tokens = [token for token in sent if token.pos_ in pos_tags and token.lemma_ not in stopwords]
	return tokens

def tokenize(text):
	nlp = spacy.load("ja_ginza")
	doc = nlp(text)

	tokens = [extract_tokens(sent) for sent in doc.sents]

	return tokens

def make_index(tokens, n):
	index = {}
	flatten_tokens = sum(tokens, [])
	len_tokens = len(flatten_tokens)
	for i, token in enumerate(flatten_tokens):

		left_text  = [flatten_tokens[i-j].text for j in range(1, min(i, n) + 1)]
		right_text = [flatten_tokens[i+j].text for j in range(1, min(len_tokens-i, n+1))]

		if token.text in index.keys():
			index[token.text].append({"index":token.idx, "left": left_text, "right":right_text})

		else:
			index[token.text] = [{"index":token.idx, "left": left_text, "right":right_text}]

	return index

def generate_nindex(INDEX_PATH, DATA_PATH, n=10):

	with open(DATA_PATH, "r", encoding="utf-8") as f:
		text = f.read()

	tokens = tokenize(text)
	index = make_index(tokens, n=n)

	with open(INDEX_PATH, "w", encoding="utf-8") as f:
		json.dump(index, f, indent=4, ensure_ascii=False)
	