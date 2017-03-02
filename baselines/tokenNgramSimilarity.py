from nltk import ngrams
import os
import nltk
import codecs

text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided/"

def getNgramFreq(n,nelems):
	ngramFreq = {}
	num = 1900
	i=0
	for chapter in os.listdir(text_dir):
		text = codecs.open(text_dir+chapter,"r",encoding="utf-8").read()
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')			
		sentences = tokenizer.tokenize(text)
		
		for sentence in sentences:
			sixgrams = ngrams(sentence.split(), n)
			for grams in sixgrams:
				ngramFreq[grams] = ngramFreq.get(grams,0) + 1

		i+=1
		if i == num:
			break

	l = sorted(ngramFreq, key=ngramFreq.get, reverse=True)[:nelems]
	return l

def generate_ngram_features(most_common_ngrams):

	text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided/"
	features = {}
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')			

	for fname in os.listdir(text_dir):
		features[fname] = {}
		features[fname]["label"] = fname.split("_")[3]
		for ngram in most_common_ngrams:
			features[fname][ngram] = 0

		text = codecs.open(text_dir+fname,"r",encoding="utf-8").read()
		sentences = tokenizer.tokenize(text)
	
		for sentence in sentences:
			Ngrams = ngrams(sentence.split(), n)
		
			for Ngram in Ngrams:
				if Ngram in most_common_ngrams:
					features[fname][Ngram] += 1 / float(len(most_common_ngrams))


	return features

def write_arff(features,name,suffix):
	arff2 = open(name+suffix+".arff","w")
	arff2.write("@relation "+ name + suffix + "\n")

	i=0
	for feats in features[features.keys()[0]]:
		if feats not in ["label","CHAR_","dp","labelProbabilities","filename"]:
			arff2.write('@attribute "w'+str(i)+'" numeric\n')
			i+=1

	labelString = "@attribute label {VirginiaWoolf,CharlesDickens,AnneBronte,CharlotteBronte,JaneAusten,MaryAnneEvans,RobertLouisStevenson,WilliamMakepeaceThackeray,MargaretOliphant,ElisabethGaskell,MariaEdgeworth,HGWells,AgathaChristie,BramStoker,JamesJoyce,LewisCarroll,ArthurConanDoyle,OscarWilde}"
	#labelString = "@attribute label {male,female}"
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


label = "LiteraryAuthor"


print 300
n=2
freqNgrams = getNgramFreq(n,300)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"2Gram300")
n=3
freqNgrams = getNgramFreq(n,300)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"3Gram300")
n=4
freqNgrams = getNgramFreq(n,300)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"4Gram300")
n=5
freqNgrams = getNgramFreq(n,300)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"5Gram300")

print label
print "2-Gram"

n=2

print 100
freqNgrams = getNgramFreq(n,100)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"2Gram100")

print 500
freqNgrams = getNgramFreq(n,500)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"2Gram500")

print 700
freqNgrams = getNgramFreq(n,700)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"2Gram700")

print 900
freqNgrams = getNgramFreq(n,900)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"2Gram900")


print "3-Gram"
n=3
print 100
freqNgrams = getNgramFreq(n,100)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"3Gram100")

print 500
freqNgrams = getNgramFreq(n,500)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"3Gram500")

print 700
freqNgrams = getNgramFreq(n,700)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"3Gram700")

print 900
freqNgrams = getNgramFreq(n,900)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"3Gram900")

print "4-Gram"
n=4
print 100
freqNgrams = getNgramFreq(n,100)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"4Gram100")

print 500
freqNgrams = getNgramFreq(n,500)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"4Gram500")

print 700
freqNgrams = getNgramFreq(n,700)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"4Gram700")

print 900
freqNgrams = getNgramFreq(n,900)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"4Gram900")


print "5-Gram"
n=5
print 100
freqNgrams = getNgramFreq(n,100)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"5Gram100")

print 500
freqNgrams = getNgramFreq(n,500)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"5Gram500")

print 700
freqNgrams = getNgramFreq(n,700)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"5Gram700")

print 900
freqNgrams = getNgramFreq(n,900)
feats=generate_ngram_features(freqNgrams)
write_arff(feats,label,"5Gram900")

exit()

'''
freqNgrams = getNgramFreq(n,300)
j=0
trainSet = {}
testSet = {}
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')			

for chapter in os.listdir(text_dir):
	text = codecs.open(text_dir+chapter,"r",encoding="utf-8").read()
	sentences = tokenizer.tokenize(text)
	
	for sentence in sentences:
		Ngrams = ngrams(sentence.split(), n)
		
		for Ngram in Ngrams:
			if Ngram in freqNgrams:
				if j < 1300:
					if chapter not in trainSet:
						trainSet[chapter] = {}
					trainSet[chapter][Ngram] = trainSet[chapter].get(Ngram,0) + 1
					
				else:
					if chapter not in testSet:
						testSet[chapter] = {}
					testSet[chapter][Ngram] = testSet[chapter].get(Ngram,0) + 1

	j+=1

for chapter, dictFeats in trainSet.iteritems():
	for freqNgram in freqNgrams:
		if freqNgram not in dictFeats:
			trainSet[chapter][freqNgram] = 0

for chapter, dictFeats in testSet.iteritems():
	for freqNgram in freqNgrams:
		if freqNgram not in dictFeats:
			testSet[chapter][freqNgram] = 0

from scipy import spatial
import operator

nPreds = len(testSet)
correct=0
for chapter, feats in testSet.iteritems():

	vectorTest = feats.values()
	realLabel = chapter.split("_")[3]
	genderScores = {}
	for chap, f in trainSet.iteritems():
		vectorTrain = f.values()
		trainLabel = chap.split("_")[3]
		score = 1 - spatial.distance.cosine(vectorTest, vectorTrain)
		genderScores[trainLabel] = genderScores.get(trainLabel,0) + score

	prediction = max(genderScores.iteritems(), key=operator.itemgetter(1))[0]
	if prediction == realLabel:
		correct+=1

print "accuracy " + str(correct/float(nPreds))'''