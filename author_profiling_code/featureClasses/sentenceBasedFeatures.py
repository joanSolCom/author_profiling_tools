# -*- coding: utf-8 -*-
from __future__ import division
import codecs
from nltk import word_tokenize
import numpy as np
import utils
import os

class SentenceBasedFeatures:

	def __init__(self,iC, modelName):
		self.iC = iC
		self.type = "SentenceBasedFeatures"
		self.iC.initFeatureType(self.type)
		self.modelName = modelName
			
	def get_wordsPerSentence_stdandrange(self):
		featureNames = [self.type+"_STD", self.type+"_Range", self.type+"_wordsPerSentence"]
		functionName = "get_wordsPerSentence_stdandrange"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			sentences = instance.sentences
			lengths = []
			for sentence in sentences:
				lengths.append(len(word_tokenize(sentence)))
			
			std = np.std(lengths)
			mean = np.mean(lengths)
			rng = np.amax(lengths) - np.amin(lengths)

			instance.addFeature(self.type, self.type+"_STD", std)
			instance.addFeature(self.type, self.type+"_Range", rng)
			instance.addFeature(self.type, self.type+"_wordsPerSentence", mean)

		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
