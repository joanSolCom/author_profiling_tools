from collections import Counter
import os
from nltk.corpus import stopwords

def generate_bow_features(most_common_words, text_dir):

	features = {}
	labels = set()
	for fname in os.listdir(text_dir):
		features[fname] = {}
		label = fname.split("_")[2]
		labels.add(label)
		features[fname]["label"] = label
		for word in most_common_words:
			features[fname][word] = 0

		tokens = open(text_dir+fname,"r").read().lower().split()
		nwords = len(tokens)

		for token in tokens:
			if token in most_common_words:
				features[fname][token] +=1 / float(nwords)

	return labels, features

def write_arff(features,name,suffix, labels):
	arff2 = open(name+suffix+".arff","w")
	arff2.write("@relation "+ name + suffix + "\n")

	i=0
	for feats in features[features.keys()[0]]:
		if feats not in ["label","CHAR_","dp","labelProbabilities","filename"]:
			featName = feats.replace('"',"DQ")
			featName = featName.replace("'","SQ")
			arff2.write('@attribute "'+featName+'" numeric\n')
			i+=1

	#labelString = "@attribute label {male,female}\n"
	strLabels = ",".join(labels)
	labelString = "@attribute label {"+ strLabels +"}"
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

	arff2.close()

text_dir = "/home/joan/Escritorio/Datasets/CCIACorpus/clean/"
arffBase = "BlogAuthor"
n_arr = [100,300,500,700,900]

all_words = []
for fname in os.listdir(text_dir):
	tokens = open(text_dir+fname,"r").read().lower().split()
	all_words.extend(tokens)

counter = Counter(all_words)

for N in n_arr:
	print N
	most_common = [i[0] for i in counter.most_common(N)]
	labels, feats = generate_bow_features(most_common, text_dir)
	write_arff(feats,arffBase,"BoW"+str(N), labels)



