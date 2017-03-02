# -*- coding: utf-8 -*-
from __future__ import division
import os
from nltk.tag.brill import Pos
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk import word_tokenize
import utils

class DictionaryBasedFeatures:
	
	def __init__(self,iC, modelName):	
		
		self.iC = iC
		self.type = "DictionaryBasedFeatures"
		self.iC.initFeatureType(self.type)
		self.load_dictionaries()
		self.modelName = modelName
	
	
	def load_dictionaries(self):
		self.abbreviationList = open("./dicts/abbreviations.txt","r").read().split()
		self.badWordsList = open("./dicts/badwords.txt","r").read().split()
		self.posList = open("./dicts/positive-words.txt","r").read().split()
		self.negList = open("./dicts/negative-words.txt","r").read().split()
		self.discourseMarkersList = open("./dicts/discourse-markers.txt","r").read().split("\n")	
		self.interjections = open("./dicts/interjections.txt").read().split("\n")
		self.depecheMood = {}
		self.loadDepecheMood()
     		
	def loadDepecheMood(self):
		depecheMood = open("./dicts/DepecheMood_normfreq.txt").read().split("\n")
		first = True
		for row in depecheMood:
			if first:
				first = False
				continue

			elements = row.split("\t")
			lemma = elements[0]
			self.depecheMood[lemma] = {}
			self.depecheMood[lemma]["afraid"] = elements[1]
			self.depecheMood[lemma]["amused"] = elements[2]
			self.depecheMood[lemma]["angry"] = elements[3]
			self.depecheMood[lemma]["annoyed"] = elements[4]
			self.depecheMood[lemma]["dont_care"] = elements[5]
			self.depecheMood[lemma]["happy"] = elements[6]
			self.depecheMood[lemma]["inspired"] = elements[7]
			self.depecheMood[lemma]["sad"] = elements[8]


	def get_discourse_markers(self):
		featureNames = [self.type+"_DiscourseMarkers"]
		functionName = "get_discourse_markers"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			content = instance.text
			words = instance.tokens
			nwords = len(words)
			nMarkers = 0
			for marker in self.discourseMarkersList:
				nApparitions = content.count(marker)
				nMarkers = nMarkers + nApparitions

			ratio = 0.0
			if nwords > 0:
				ratio = nMarkers / nwords

			instance.addFeature(self.type, self.type+"_DiscourseMarkers", ratio)	
		
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
	
	def get_dict_count(self):		
		featureNames = [self.type+"_Abbrev", self.type+"_Curse", self.type+"_Positive", self.type+"_Negative"]
		functionName = "get_dict_count"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			lWords = instance.tokens
			nwords = len(lWords)
			nAbbrev = 0
			nCurse = 0
			nPos = 0
			nNeg = 0
			ratioAbbrev = 0.0
			ratioCurse = 0.0
			ratioPos = 0.0
			ratioNeg = 0.0

			for word in lWords:
				word = word.lower()
				if word in self.abbreviationList:
					nAbbrev = nAbbrev + 1
				if word in self.badWordsList:
					nCurse = nCurse + 1
				if word in self.negList:
					nNeg = nNeg + 1
				if word in self.posList:
					nPos = nPos + 1

			if nwords > 0:
				ratioAbbrev = nAbbrev / nwords
				ratioCurse = nCurse / nwords
				ratioPos = nPos / nwords
				ratioNeg = nNeg / nwords
				
			instance.addFeature(self.type, self.type+"_Abbrev", ratioAbbrev)
			instance.addFeature(self.type, self.type+"_Curse", ratioCurse)
			instance.addFeature(self.type, self.type+"_Positive", ratioPos)
			instance.addFeature(self.type, self.type+"_Negative", ratioNeg)
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
			
	def get_interjections(self):
		featureNames = [self.type+"_Interjections"]
		functionName = "get_interjections"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			content = instance.text
			nwords = len(instance.tokens)
			nInterjections = 0
			ratio = 0.0

			for interjection in self.interjections:
				if content.count(interjection.lower()) > 0:
					nInterjections +=content.count(interjection.lower())

			if nwords > 0:
				ratio = nInterjections / float(nwords)

			instance.addFeature(self.type, self.type+"_Interjections", ratio)
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
							
	def get_mean_mood(self):
		featureNames = [self.type+"_TokenRatioAfraid", self.type+"_TokenRatioAmused", self.type+"_TokenRatioAngry", self.type+"_TokenRatioAnnoyed", self.type+"_TokenRatioDontCare", self.type+"_TokenRatioHappy", self.type+"_TokenRatioInspired", self.type+"_TokenRatioSad", self.type+"_EmotionRatio",self.type+"_EmotionRatioAfraid", self.type+"_EmotionRatioAmused", self.type+"_EmotionRatioAngry", self.type+"_EmotionRatioAnnoyed", self.type+"_EmotionRatioDontCare", self.type+"_EmotionRatioHappy", self.type+"_EmotionRatioInspired", self.type+"_EmotionRatioSad"]
		functionName = "get_mean_mood"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return


		lmtzr = WordNetLemmatizer()

		for instance in self.iC.instances:
			tokens = instance.tokens
			totalTokens = len(tokens)
			text_tagged = nltk.pos_tag(tokens)

			totalAfraid = 0
			totalAmused = 0
			totalAngry = 0
			totalAnnoyed = 0
			totalDontCare = 0
			totalHappy = 0
			totalInspired = 0
			totalSad = 0
			totalEmotionTokens = 0

			ratioAfraid = 0.0
			ratioAmused = 0.0
			ratioAngry = 0.0
			ratioAnnoyed = 0.0
			ratioDontCare = 0.0
			ratioHappy = 0.0
			ratioInspired = 0.0
			ratioSad = 0.0
			ratioEmotionTokens = 0.0

			ratioEAfraid = 0.0
			ratioEAmused = 0.0
			ratioEAngry = 0.0
			ratioEAnnoyed = 0.0
			ratioEDontCare = 0.0
			ratioEHappy = 0.0
			ratioEInspired =0.0
			ratioESad = 0.0
			
			for word in text_tagged:
				pos = self.getDepecheMoodPos(word[1])
				if pos is None:
					continue
				
				if pos == "v":
					lemma = lmtzr.lemmatize(word[0], "v")
				else:
					lemma = lmtzr.lemmatize(word[0])
				
				lemma = lemma.lower()

				idx = lemma+"#"+pos

				if idx in self.depecheMood.keys():
					totalEmotionTokens+=1
					totalAfraid += float(self.depecheMood[idx]["afraid"])
					totalAmused += float(self.depecheMood[idx]["amused"])
					totalAngry += float(self.depecheMood[idx]["angry"])
					totalAnnoyed += float(self.depecheMood[idx]["annoyed"])
					totalDontCare += float(self.depecheMood[idx]["dont_care"])
					totalHappy += float(self.depecheMood[idx]["happy"])
					totalInspired += float(self.depecheMood[idx]["inspired"])
					totalSad += float(self.depecheMood[idx]["sad"])

			if totalTokens > 0:
				ratioAfraid = totalAfraid / totalTokens
				ratioAmused = totalAmused / totalTokens
				ratioAngry = totalAngry / totalTokens
				ratioAnnoyed = totalAnnoyed / totalTokens
				ratioDontCare = totalDontCare / totalTokens
				ratioHappy = totalHappy / totalTokens
				ratioInspired = totalInspired / totalTokens
				ratioSad = totalSad / totalTokens
				ratioEmotionTokens = totalEmotionTokens / totalTokens

			instance.addFeature(self.type, self.type+"_TokenRatioAfraid", ratioAfraid)
			instance.addFeature(self.type, self.type+"_TokenRatioAmused", ratioAmused)
			instance.addFeature(self.type, self.type+"_TokenRatioAngry", ratioAngry)
			instance.addFeature(self.type, self.type+"_TokenRatioAnnoyed", ratioAnnoyed)
			instance.addFeature(self.type, self.type+"_TokenRatioDontCare", ratioDontCare)
			instance.addFeature(self.type, self.type+"_TokenRatioHappy", ratioHappy)
			instance.addFeature(self.type, self.type+"_TokenRatioInspired", ratioInspired)
			instance.addFeature(self.type, self.type+"_TokenRatioSad", ratioSad)
			instance.addFeature(self.type, self.type+"_EmotionRatio", ratioEmotionTokens)


			if totalEmotionTokens > 0:
				ratioEAfraid = totalAfraid / totalEmotionTokens
				ratioEAmused = totalAmused / totalEmotionTokens
				ratioEAngry = totalAngry / totalEmotionTokens
				ratioEAnnoyed = totalAnnoyed / totalEmotionTokens
				ratioEDontCare = totalDontCare / totalEmotionTokens
				ratioEHappy = totalHappy / totalEmotionTokens
				ratioEInspired = totalInspired / totalEmotionTokens
				ratioESad = totalSad / totalEmotionTokens

			instance.addFeature(self.type, self.type+"_EmotionRatioAfraid", ratioEAfraid)
			instance.addFeature(self.type, self.type+"_EmotionRatioAmused", ratioEAmused)
			instance.addFeature(self.type, self.type+"_EmotionRatioAngry", ratioEAngry)
			instance.addFeature(self.type, self.type+"_EmotionRatioAnnoyed", ratioEAnnoyed)
			instance.addFeature(self.type, self.type+"_EmotionRatioDontCare", ratioEDontCare)
			instance.addFeature(self.type, self.type+"_EmotionRatioHappy", ratioEHappy)
			instance.addFeature(self.type, self.type+"_EmotionRatioInspired", ratioEInspired)
			instance.addFeature(self.type, self.type+"_EmotionRatioSad", ratioESad)
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)

				
	def getDepecheMoodPos(self,nltkPos):
		
		if nltkPos.startswith("V"):
			return "v"
		elif nltkPos.startswith("N"):
			return "n"
		elif nltkPos.startswith("J"):
			return "a"
		elif nltkPos.startswith("R"):
			return "r"
		else:
			return None
				
			
			