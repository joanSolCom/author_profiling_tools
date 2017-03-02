from sklearn.model_selection import KFold
import numpy as np
import os
from collections import Counter
from sklearn.svm import SVC
from sklearn.preprocessing import scale

pathData = "/home/joan/Escritorio/Datasets/blogAuthorshipCorpus/clean/"

def generate_bow_features(most_common_words, fnames, X):

	features = {}
	labels = set()
	for findex in fnames:
		fname = X[findex][0]
		features[fname] = {}
		label = fname.split(".")[1]
		labels.add(label)
		features[fname]["label"] = label
		for word in most_common_words:
			features[fname][word] = 0

		tokens = open(pathData+fname,"r").read().lower().split()
		nwords = len(tokens)

		for token in tokens:
			if token in most_common_words:
				features[fname][token] +=1 / float(nwords)

	return labels, features

def getSklearnInput(features):
	
	featureOrder = sorted(features[features.keys()[0]].keys())
	X = []
	Y = []

	for fname, featDict in features.iteritems():
		x = []
		y = []
		for f in featureOrder:
			if f != "label":
				x.append(featDict[f])
			else:
				y.append(featDict[f])

		X.append(x)
		Y.append(y)

	return X, Y


X = []
Y = []

for fname in os.listdir(pathData):
	X.append([fname])
	Y.append(fname.split(".")[1])

X = np.array(X)
Y = np.array(Y)

kf = KFold(n_splits=10)
kf.get_n_splits(X)
foldIdx=1
for train_index, test_index in kf.split(X):
	print "FOLD NUMBER " + str(foldIdx)
	clf = SVC()

	all_words_train = []
	for findex in train_index:
		fname = X[findex][0]
		tokens = open(pathData+fname,"r").read().lower().split()
		all_words_train.extend(tokens)

	counter = Counter(all_words_train)
	most_common_train = [i[0] for i in counter.most_common(500)]
	_, features_train = generate_bow_features(most_common_train, train_index, X)
	X_train, Y_train = getSklearnInput(features_train)
	X_train_norm = scale(X_train, axis=0, with_mean=True, with_std=True, copy=True)

	_, features_test = generate_bow_features(most_common_train, test_index, X)
	X_test, Y_test = getSklearnInput(features_test)
	X_test_norm = scale(X_test, axis=0, with_mean=True, with_std=True, copy=True)

	clf.fit(X_train_norm, Y_train)
	print clf.score(X_test_norm, Y_test)
	foldIdx+=1
	exit()