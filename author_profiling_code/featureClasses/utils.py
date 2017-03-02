import re
import codecs


def get_words_from_file(path):
	with codecs.open(path, 'r',encoding="latin1") as inf:
		return inf.read().split()

def get_words_from_string(s):
	return re.findall(re.compile('\w+'), s.lower())

def get_words_from_article(self,path,lower = True):
	words = get_words_from_file(path)
	lWords = {}
	for word in words:
		if lower:
			word = word.lower()
		key = lWords.get(word)
		
		if key is None:
			lWords[word] = 1
		else:
			lWords[word] = lWords[word] + 1

	lWords = sorted(lWords.items(), key=lambda x: x[1],reverse=True)
	return lWords


def load_features_from_file(path, iC, featureType):

	fd = open(path,"r")
	f = fd.read().split("---\n")
	for block in f:
		features = block.split("\n")
		post = features[0]

		for feat in features:
			pieces = feat.split("->")
			if len(pieces)>1:
				if iC.instanceDict[post] is not None:
					try:
						iC.instanceDict[post].addFeature(featureType, pieces[0], float(pieces[1]))
					except ValueError:
						print pieces
						exit()
	fd.close()

#lFeats is the list of features to save to the file, the keys of self.features to visit.
def save_features_to_file(name,lFeats,iC, featureType):
	f = open(name,"w")

	for name, instance in iC.instanceDict.iteritems():
		f.write(name + "\n")
		for feat in lFeats:
			f.write(feat + "->" + str(instance.featureSet.featureDict[featureType][feat].value) + "\n")
		f.write("---"+"\n")
	
	f.close()