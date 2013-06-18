common_words_file = open("common_words.txt")
common_words = []
with open(common_words_file) as f:
    common_words = f.readlines()

def classify(note):
	categories = []
	for word in note:
		if word.lower() in common_words:
			categories.append(word)
	return categories

