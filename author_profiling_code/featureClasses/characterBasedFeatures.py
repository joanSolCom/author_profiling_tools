# -*- coding: utf-8 -*-
from __future__ import division
import os
import re
from nltk import word_tokenize
import codecs
import utils

class CharacterBasedFeatures:

	def __init__(self,iC, modelName):
		self.iC = iC
		self.type = "CharacterBasedFeatures"
		self.iC.initFeatureType(self.type)
		self.modelName = modelName

	def get_uppers(self):
		featureNames = [self.type+"_UpperCases"]
		functionName = "get_uppers"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			featValue = 0.0
			matches = re.findall("[A-Z]",instance.text,re.DOTALL)
			upperCases = len(matches)
			ratio = upperCases / len(instance.text)
			instance.addFeature(self.type, self.type+"_UpperCases", ratio)

		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)


	def get_in_parenthesis_stats(self):

		featureNames = [self.type+"_charsinparenthesis", self.type+"_wordsinparenthesis"]
		functionName = "get_in_parenthesis_stats"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			matches = re.findall("\((.*?)\)", instance.text)
			npar = len(matches)
			totalchars = 0
			totalwords = 0

			for match in matches:
				totalchars += len(match)
				words = word_tokenize(match)
				totalwords = len(words)

			charsInParenthesis = 0.0
			wordsInParenthesis = 0.0
			if npar > 0:
				charsInParenthesis = totalchars / npar
				wordsInParenthesis = totalwords / npar

			instance.addFeature(self.type, self.type+"_charsinparenthesis", charsInParenthesis)
			instance.addFeature(self.type, self.type+"_wordsinparenthesis", wordsInParenthesis)
		
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)


	def get_numbers(self):
		featureNames = [self.type+"_Numbers"]
		functionName = "get_numbers"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			matches = re.findall("[0-9]", instance.text)
			ratio = 0.0
			nchars = len(instance.text)

			if nchars > 0:
				ratio = len(matches) / nchars

			instance.addFeature(self.type, self.type+"_Numbers", ratio)
		
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
		
	def get_symbols(self,symbols, featureName):
		featureNames = [self.type+"_"+featureName]
		functionName = "get_symbols_"+featureName

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			nChars = len(instance.text)
			matches = 0
			ratio = 0.0
			
			for char in instance.text:
				if char in symbols:
					matches = matches + 1
			
			if nChars > 0:
				ratio = matches / nChars

			instance.addFeature(self.type, self.type+"_"+featureName, ratio)

		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
       