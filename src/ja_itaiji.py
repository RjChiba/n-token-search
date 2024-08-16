import os, sys
import json

CRR_DIR = os.path.dirname(os.path.abspath(__file__))
ITAIJI_PATH = os.path.join(CRR_DIR, "./data/term/ja-itaiji.json")

class Itaiji:
	"""Handle itaiji (異体字)
	
	Attributes:
	    dictionary (dict): itaiji list
	"""
	
	dictionary = {}
	with open(ITAIJI_PATH, "r", encoding="utf-8") as f:
		dictionary = json.load(f)

	@staticmethod
	def get_family(target):
		"""Summary
		
		Args:
		    target (str): objective string
		
		Returns:
		    list(str): string list equivalent to target
		"""
		return Itaiji.dictionary.get(target, [target])

	@staticmethod
	def is_family(kanji1, kanji2):
		"""Summary
		
		Args:
		    kanji1 (str): kanji to check
		    kanji2 (str): kanji to check
		
		Returns:
		    bool: whether kanji1 and kanji2 are equivarent
		"""
		if kanji1 == kanji2:
			return True

		return bool(kanji1 in Itaiji.dictionary.get(kanji2, []))

	@staticmethod
	def is_similar(word1, word2):
		"""Summary
		
		Args:
		    word1 (str): word to check
		    word2 (str): word to check
		
		Returns:
		    bool: whether word1 and word2 are equivarent within itaiji
		"""
		# F-case: length mismatch
		if len(word1) != len(word2):
			return False

		# T-case: same word
		if word1 == word2:
			return True

		# check similarity
		for i in range(len(word1)):
			if Itaiji.is_family(word1[i], word2[i]):
				pass
			else:
				return False

		return True

	@staticmethod
	def get_similar(word, n=-1):
		"""get word list replacing each kanji with its itaiji
		
		Args:
		    word (str): original word
		    n (int, optional): maximum time to replace kanji
		
		Returns:
		    list(str): list of replaced words
		"""

		# kanji swap limit (max: len(word))
		n = len(word) if n == -1 else n
		
		words = [[0, ""]]

		for kanji in word:
			kanji_family = Itaiji.get_family(kanji)
			new_words = []
			for w in words:
				for i, k in enumerate(kanji_family):
					c = 0 if i == 0 else 1
					
					if w[0]+c > n:
						break
					
					new_words.append([w[0]+c, w[1]+k])

			words = new_words

		return list(map(lambda x: x[1], words))
