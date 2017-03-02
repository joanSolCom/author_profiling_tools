from collections import Counter
import os
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

class LexicalFeatures:

	def __init__(self,iC, modelName):
		self.iC = iC
		self.type = "LexicalFeatures"
		self.iC.initFeatureType(self.type)
		self.modelName = modelName

	def generate_bow_features(self, nwords):

		all_words = []

		for instance in self.iC.instances:
			tokens = instance.lowerTokens
			for idx, token in enumerate(tokens):
				token = token.replace("'","")
				token = token.replace('"',"")
				token = token.replace(",","")
				token = token.replace(".","")
				token = token.replace("-","")
				token = token.replace(":","")
				token = token.replace(";","")
				token = token.replace("_","")
				token = token.replace("!","")
				token = token.replace("?","")
				tokens[idx] = token
			all_words.extend(tokens)

		counter = Counter(all_words)
		most_common = [i[0] for i in counter.most_common(nwords)]

		for word in most_common:
			for instance in self.iC.instances:
				ratio = 0.0
				tokens = instance.lowerTokens
				nwords = len(tokens)
				for token in tokens:
					if token == word:
						ratio += 1 / float(nwords)
			
				instance.addFeature(self.type, self.type+"_"+word, ratio)


	def get_bow_tfidf(self, N):

		count_vect = CountVectorizer(analyzer="word")
		docs = []
		for instance in self.iC.instances:
			raw = instance.text
			docs.append(raw)

		X_train_counts = count_vect.fit_transform(docs)
		tfidf_transformer = TfidfTransformer(norm='l1', use_idf=True, smooth_idf=True, sublinear_tf=False)
		X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

		feature_array = np.array(count_vect.get_feature_names())
		tfidf_sorting = np.argsort(X_train_tfidf.toarray()).flatten()[::-1]

		top_n = feature_array[tfidf_sorting][:N]

		for word in top_n:
			for instance in self.iC.instances:
				ratio = 0.0
				tokens = instance.lowerTokens
				nwords = len(tokens)
				for token in tokens:
					if token == word:
						ratio += 1 / float(nwords)
			
				instance.addFeature(self.type, self.type+"_"+word, ratio)



