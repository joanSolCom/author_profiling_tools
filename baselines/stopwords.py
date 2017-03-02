from collections import Counter
import os
from nltk.corpus import stopwords

def generate_stopword_features(stopwordList):

	text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided/"
	features = {}
	nProcessed = 0
	fnames = os.listdir(text_dir)
	nElems = len(fnames)

	for fname in fnames:
		features[fname] = {}
		features[fname]["label"] = fname.split("_")[3]
		for word in stopwordList:
			features[fname][word] = 0

		tokens = open(text_dir+fname,"r").read().lower().split()
		nTokens = len(tokens)
		for token in tokens:
			if token in stopwordList:
				features[fname][token] += 1/float(nTokens)

		nProcessed+=1
		print "Processed " + str(nProcessed) + " of " + str(nElems)

	return features

def getLabels(features):
	labels = []
	for key, feats in features.iteritems():
		label = feats["label"]
		if label not in labels:
			labels.append(label)

	return labels

def write_arff(features,name,suffix):
	arff2 = open(name+suffix+".arff","w")
	arff2.write("@relation "+ name + suffix + "\n")

	i=0
	for feats in features[features.keys()[0]]:
		if feats not in ["label","CHAR_","dp","labelProbabilities","filename"]:
			arff2.write('@attribute "w'+str(i)+'" numeric\n')
			i+=1

	labels = getLabels(features)
	labelString = "@attribute label {"
	for label in labels:
		labelString+=label+","
	labelString = labelString[:-1]
	labelString+="}\n"

	arff2.write(labelString)
	arff2.write("\n@data\n")

	for key,value in features.iteritems():
		n = 0
		for key2,value2 in value.iteritems():
			n = n + 1
			if key2 not in ["label","labelProbabilities","filename"]:
				arff2.write(str(value2)+",")
				if n == len(value):
					arff2.write(str(value['label']) + "\n")

featsStopwords = generate_stopword_features(stopwords.words('english'))
write_arff(featsStopwords,"Literary","stopwordsAuthor")