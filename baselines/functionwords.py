from __future__ import division
from collections import Counter
import os
from nltk.corpus import stopwords
import nltk
import codecs


def init_features():
	text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided_american/"
	features = {}
	nProcessed = 0
	fnames = os.listdir(text_dir)
	nElems = len(fnames)
	for fname in fnames:
		label = fname.split("_")[1]
		features[fname] = {}
		features[fname]["label"] = label

	return features


def generate_stopword_features(features,stopwordList):
	text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided_american/"
	for fname in features.keys():
		for word in stopwordList:
			features[fname][word] = 0

		tokens = open(text_dir+fname,"r").read().lower().split()
		nTokens = len(tokens)
		for token in tokens:
			if token in stopwordList:
				features[fname][token] += 1/float(nTokens)

	return features

def generate_pos_features(features):
	text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided_american/"
	posRelations = []

	for fname in features.keys():
		tokens = codecs.open(text_dir+fname,"r",encoding="utf-8").read().lower().split()
		ntokens = len(tokens)
		text_tagged = nltk.pos_tag(tokens)
		for token,pos in text_tagged:
			if pos not in features[fname]:
				features[fname][pos] = 0
			
			if pos not in posRelations:
				posRelations.append(pos)

			features[fname][pos] += 1/ntokens

	for fname in features.keys():
		for posRel in posRelations:
			if posRel not in features[fname]:
				features[fname][posRel] = 0.0

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
			arff2.write('@attribute "w'+str(i)+"_"+feats+'" numeric\n')
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

fwordraw = open("functionWords.txt","r").read().split("\n")
fwordList = []
for line in fwordraw:
	fword = line.split()[0]
	fwordList.append(fword)

#stopwords = nltk.corpus.stopwords.words('english')
features = init_features()
features = generate_pos_features(features)
features = generate_stopword_features(features, fwordList)
write_arff(features,"LiteraryAmerican","FwordsPoSGender")