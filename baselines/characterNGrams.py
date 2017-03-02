import os
import codecs
import operator

dataset_path = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided/"
trPostPerAuth = {}
posts = []
ngrams = {}
N = 2

def get_char_ngrams(N,text):
	charngramstext = []
	for i in range(len(text)-N+1):
		charngramstext.append(text[i:i+N])
	return charngramstext

def fill_ngrams(N,text,ngrams):
	cngrs = get_char_ngrams(N,text)
	
	for cngr in cngrs:
		if cngr in ngrams.keys():
			ngrams[cngr]+=1
		else:
			ngrams[cngr] = 1
	
	return ngrams

def select_ngrams(ngrams,num):
	sorted_ngrams = sorted(ngrams.items(), key=operator.itemgetter(1))
	return sorted_ngrams[:num]
	

for f in os.listdir(dataset_path):
	if len(f) < 2:
		continue

	author = f.split("_")[3]
	text = codecs.open(dataset_path + "/" + f,"r",encoding="utf8").read()
	ngrams = fill_ngrams(N,text,ngrams)
	posts.append(f)


def featuresToArff(features,name,suffix):
	arff2 = open(name+suffix+".arff","w")
	arff2.write("@relation "+ name + suffix + "\n")
	labels = []
	for feats,vals in features[features.keys()[0]].iteritems():
		if feats != "label":
			arff2.write('@attribute "'+str(feats)+'" numeric\n')

	labelString = "@attribute label {VirginiaWoolf,CharlesDickens,AnneBronte,CharlotteBronte,JaneAusten,MaryAnneEvans,RobertLouisStevenson,WilliamMakepeaceThackeray,MargaretOliphant,ElisabethGaskell,MariaEdgeworth,HGWells,AgathaChristie,BramStoker,JamesJoyce,LewisCarroll,ArthurConanDoyle,OscarWilde}"
	labelString+="}\n"
	
	arff2.write(labelString)
	arff2.write("\n@data\n")
	init = False
	for key,value in features.iteritems():
		for key2,value2 in value.iteritems():
			arff2.write(str(value2)+",")
		
		l = key.split("_")[1]		
		arff2.write(l + "\n")

ngrams = select_ngrams(ngrams,200)
features = {}

for f in posts:
	features[f] = {}
	for ngram in ngrams:
		features[f][ngram] = 0
		
	text = codecs.open(dataset_path + "/" + f,"r",encoding="utf8").read()
	ngrs = get_char_ngrams(N,text)
	for ngr in ngrs:
		if ngr in ngrams:
			features[f][ngr]+=1
			
featuresToArff(features,"LiteraryAuthor","2Grams")