from featureManager import FeatureSet
import os
import numpy as np
from nltk import word_tokenize
import codecs
import nltk

def createInstanceCollection(paths, labelPosition=1, separator = "_", selectedLabels = None):
	iC = InstanceCollection()
	for fname in os.listdir(paths["clean"]):
		pieces = fname.split(separator)
		label = pieces[labelPosition]
		if selectedLabels:
			if label in selectedLabels:
				instance = Instance(fname, label, paths)
				iC.addInstance(instance)
		else:
			instance = Instance(fname, label, paths)
			iC.addInstance(instance)

	return iC


class Instance:

	def __init__(self, name, label, paths):
		self.name = name
		self.featureSet = FeatureSet()
		self.label = label
		
		pathsUpdated = {}
		for category, pathBase in paths.iteritems():
			pathsUpdated[category] = pathBase + self.name

		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')	

		self.paths = pathsUpdated
		self.text = codecs.open(self.paths["clean"],"r", encoding="utf-8").read()

		if "synParsed" in self.paths:
			self.conll = codecs.open(self.paths["synParsed"],"r", encoding="utf-8").read()
		else:
			self.conll = None
		if "discParsed" in self.paths:
			self.discourse = codecs.open(self.paths["discParsed"],"r", encoding="utf-8").read()
		else:
			self.discourse = None

		self.tokens = word_tokenize(self.text)
		self.lowerTokens = self.text.lower().split()
		self.sentences = tokenizer.tokenize(self.text)

	def getFeaturenames(self, featuresSelected):
		return self.featureSet.getFeaturenames(featuresSelected)

	def getFeatureTypeNames(self, featuresSelected):
		return self.featureSet.getFeatureTypeNames(featuresSelected)

	def getFeatureVector(self, featuresSelected):
		return self.featureSet.getFeatureVector(featuresSelected)

	def initFeatureType(self, featureType):
		self.featureSet.initFeatureType(featureType)

	def addFeature(self, featureType, featureName, featureValue):
		self.featureSet.addFeature(featureType, featureName, featureValue)

	def updateFeature(self, featureType, featureName, increment, operation="sum"):
		self.featureSet.updateFeature(featureType, featureName, increment, operation)

	def __repr__(self):
		return self.name + "\n" + self.label+ "\n" + str(self.featureSet) #+ "\n"+str(self.tokens)

class InstanceCollection:

	def __init__(self):
		self.instances = []
		self.labels = set()
		self.instanceDict = {}
		self.featurePath = "/home/joan/repository/PhD/BESTVersion/precalculated/features/"

	def __repr__(self):
		strCollection = ""
		for instance in self.instances:
			strCollection += "---------\n"+ str(instance) +"\n---------"
		return strCollection

	def initFeatureType(self, featureType):
		for instance in self.instances:
			instance.initFeatureType(featureType)

	def addInstance(self, instance):
		self.instances.append(instance)
		self.instanceDict[instance.name] = instance
		self.labels.add(instance.label)


	def getFeatureNames(self, featuresSelected):
		return self.instances[0].getFeatureNames(featuresSelected)

	def getFeatureTypeNames(self, featuresSelected):
		return self.instances[0].getFeatureTypeNames(featuresSelected)


	def getSklearnInput(self, featuresSelected = None):
		X = []
		Y = []

		featureTypeNames = self.getFeatureTypeNames(featuresSelected)

		for instance in self.instances:
			featureVector = instance.getFeatureVector(featureTypeNames)
			X.append(featureVector)
			Y.append(instance.label)

		return X, Y

	def getMeanFeatValuesPerClass(self, featuresSelected=None):
		featureTypeNames = self.getFeatureTypeNames(featuresSelected)
		nFeats = len(featureTypeNames)

		dictPerClass = {}

		for instance in self.instances:
			featureVector = instance.getFeatureVector(featureTypeNames)
			label = instance.label
			if label not in dictPerClass:
				dictPerClass[label] = np.array([featureVector],dtype=np.float64)
			else:
				dictPerClass[label] = np.append(dictPerClass[label],[featureVector],axis=0)

		outDict = {}
		for label, matrix in dictPerClass.iteritems():
			i=0
			outDict[label] = {}
			while i < nFeats:
				
				featureValues = matrix[:,i]
				featureType, featureName = featureTypeNames[i]
				
				mean = np.mean(featureValues)
				median = np.median(featureValues)
				std = np.std(featureValues)
				
				outDict[label][featureName] = {}
				outDict[label][featureName]["mean"] = mean
				outDict[label][featureName]["median"] = median
				outDict[label][featureName]["std"] = std

				i+=1

		return outDict

	def getArffString(self, fname, featuresSelected = None, selectedLabels = None):
		arffString = "@relation "+ fname+ "\n"
		featureTypeNames = self.getFeatureTypeNames(featuresSelected)

		for featType,featName in featureTypeNames:
			featName = featName.replace('"',"DQ")
			featName = featName.replace("'","SQ")
			arffString += '@attribute "'+featName+'" numeric\n'

		labelString = "@attribute label {"
		if not selectedLabels:
			labels = self.labels
		else:
			labels = selectedLabels
		j=0
		for label in labels:
			j+=1
			if j < len(labels):
				labelString+=label+","
			elif j == len(labels):
				labelString+=label

		labelString+="}\n"
		arffString += labelString
		arffString += "\n@data\n"

		for instance in self.instances:
			if selectedLabels:
				if instance.label in selectedLabels:
					featVector = instance.getFeatureVector(featureTypeNames)
					featVector = map(str, featVector)    
					arffString += ",".join(featVector)
					arffString += "," + instance.label + "\n"
			else:
				featVector = instance.getFeatureVector(featureTypeNames)
				featVector = map(str, featVector)    
				arffString += ",".join(featVector)
				arffString += "," + instance.label + "\n"

		return arffString


	def toArff(self, path, fname ,featuresSelected = None, selectedLabels=None):
		arffString = self.getArffString(fname,featuresSelected, selectedLabels)
		fd = open(path+fname,"w")
		fd.write(arffString.encode("utf-8"))
		fd.close()
		
	