from bisect import *

common_words_file = open("common_words.txt")
common_words = []
with open(common_words_file) as f:
    common_words = f.readlines()

def classify(note):
	categories = []
	if bisect_right(common_words, word.lower()) != 0:
		categories.append(word.lower())
	return categories


