import os, sys
import json

import spacy
from ja_itaiji import Itaiji

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

def search_idx(INDEX_PATH, search_text):
	# load index data
	with open(INDEX_PATH, "r", encoding="utf-8") as fp:
		index_data = json.load(fp)

	# tokenize and extract search_text
	search_tokens = tokenize(search_text)

	# result index
	idx = []

	# search token
	flatten_tokens = sum(search_tokens, [])
	print("search tokens:", flatten_tokens)

	for i, token in enumerate(flatten_tokens):
		token_text = token.text

		left_token  = flatten_tokens[:i]
		right_token = flatten_tokens[i+1:]

		# get index list (itaiji match)
		itaiji_texts = Itaiji.get_similar(token_text)
		token_texts = index_data.keys()
		token_index = []

		for itaiji_text in itaiji_texts:

			if itaiji_text in token_texts:
				token_index = index_data.get(itaiji_text, [])

		for index in token_index:
			l = 0
			r = 0

			# left search (maximum match)
			while True:
				try:
					if Itaiji.is_similar(left_token[l].text, index["left"][::-1][l]):
						l += 1
					else:
						break

				except IndexError:
					break

			# right search (maximum match)
			while True:
				try:
					if Itaiji.is_similar(right_token[r].text, index["right"][r]):
						r += 1
					else:
						break

				except IndexError:
					break

			# result priority: matched rate (based on tokens)
			priority = (l + r + 1) / len(flatten_tokens)

			is_unique = all([index["index"] <= i[1] or i[1] + len(search_text) <= index["index"] for i in idx])

			if priority != 0 and is_unique:
				idx.append((priority, index["index"]))

	idx = sorted(idx, key=lambda x: x[0])
	return idx

def get_sentence(text, idx, length=200):

	start = max(idx - length//2, 0)
	end   = min(idx + length//2, len(text))

	return text[start:end]

def search(INDEX_PATH, DATA_PATH, search_text, length=40):
	idx = search_idx(INDEX_PATH, search_text)

	with open(DATA_PATH, "r", encoding="utf-8") as f:
		text = f.read()

	res = []
	for i in idx:
		res.append([i[0], get_sentence(text, i[1], length=length)])

	return res