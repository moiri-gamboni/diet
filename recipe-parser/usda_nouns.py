from __future__ import print_function
from nltk import pos_tag, word_tokenize
import textblob, json
text = []
usda = {}
with open('USDA-food-db/usda-reduced.json') as f:
	for line in f:
		ingredient = json.loads(line)
		usda[ingredient["name"]["long"]] = ingredient

translation = {}
print("Getting text")
for ingredient in usda:
	text.append(ingredient)
	text.append(ingredient.lower())
	text.append("I eat "+ingredient+".")
	text.append("I eat "+ingredient.lower()+".")
	text.append(ingredient+" tastes good.")
	text.append(ingredient.lower()+" tastes good.")
	translation[ingredient.lower()] = ingredient

tags = []
done = 0.0
print("Getting tags")
for phrase in text:
	tags.append((phrase, "NLTK", [tag[0].lower() for tag in pos_tag(word_tokenize(phrase)) if tag[1] in ["NN","NNP","NNS", "NNPS", "NP"] and len(tag[0].lower())>1]))
	tags.append((phrase, "TextBlob", [tag[0].lower() for tag in textblob.TextBlob(phrase).tags if tag[1] in ["NN","NNP","NNS", "NNPS", "NP"] and len(tag[0].lower())>1]))
	done += 1
	print("%.1f %%" % (100*done/len(text)))

nltk_nouns = {}
textblob_nouns = {}

print("Grouping tags")
for tag in tags:
	if "I eat " in tag[0]:
		key = tag[0][6:-1].lower()
	elif " tastes good." in tag[0]:
		key = tag[0][:-13].lower()
	else:
		key = tag[0].lower()
	if tag[1] == "NLTK":
		if key not in nltk_nouns:
			nltk_nouns[key] = set()
		nltk_nouns[key].update(tag[2])
	else:
		if key not in textblob_nouns:
			textblob_nouns[key] = set()
		textblob_nouns[key].update(tag[2])

print("Adding tags")
done = 0.0
for ingredient in nltk_nouns:
	usda[translation[ingredient]]["name"]["split"] = list(nltk_nouns[ingredient].union(textblob_nouns[ingredient]))

print("Saving USDA")
with open("USDA-food-db/usda-full.json", 'wb+') as f:
	for ingredient_name, ingredient in usda.iteritems():
		f.write(json.dumps(ingredient)+'\n')

