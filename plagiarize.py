from nltk import word_tokenize, pos_tag
import requests

accepted_pos = {'NN': '(noun)', 'NNS': '(noun)', 'RB': '(adv)', 'RBR': '(adv)', 'RBS': '(adv)', 'RP': 'particle', 'VB': '(verb)', 'VBN': '(verb)', 'VBZ': '(verb)', 'VBN': '(verb)', 'VBG': '(verb)', 'VBD': '(verb)', 'VBP': '(verb)', 'VBZ': '(verb)', 'JJ': '(adj)', 'JJR': '(adj)', 'JJS': '(adj)'}
def parse_word(msg, key):
	# Obtain a list of tuples formatted as (pos, word)
	pos_words = [pair[::-1] for pair in pos_tag(word_tokenize(msg))]
	for pos, word in pos_words:
		if pos in accepted_pos.keys():
			print((pos, word))
			# API Query
			try:
				response = requests.get(f"http://thesaurus.altervista.org/thesaurus/v1?key={key}&word={word}&language=en_US&output=json").json()
			except KeyError:
				return 'Could not query API!'
			try: 
				for item in response['response']:
					if item['list']['category'] == accepted_pos[pos]:
						new_word = item['list']['synonyms'].split('|')[0]
						# Filtering 'noted' responses
						startIndex = new_word.find(' (')
						new_word = new_word[:startIndex:] if startIndex != -1 else new_word
						print(new_word)
						break
					else:
						print('passed')
						new_word = word
				# Replace word with new_word in tokenized list
				pos_words[pos_words.index((pos, word))] = (pos, new_word)
			except KeyError:
				print('passed')
				pass
	# Hacky solution to reformat, but good for now
	return ' '.join([word for pos, word in pos_words]).replace(' .', '.').replace(' ,', ',').replace(' ?', '?').replace(' !', '!').replace(' ;', ';').replace(' "', '"').replace('" ', '"')

# Tests
# print(parse_word('“Mind,” he began again, lifting one arm from the elbow, the palm of the hand outwards, so that, with his legs folded before him, he had the pose of a Buddha preaching in European clothes and without a lotus-flower—“Mind, none of us would feel exactly like this.'))
