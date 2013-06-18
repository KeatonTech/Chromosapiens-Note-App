common_words = open("common_words.txt")

def classify(note):
	categories = []
	for word in note:
		if word.lower() in common_words:
			categories.append(word)
	return categories

	