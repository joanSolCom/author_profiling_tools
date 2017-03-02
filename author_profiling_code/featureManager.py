class Feature:

	def __init__(self, featureName, featureValue):
		self.name = featureName
		self.value = featureValue

	def __repr__(self):
		return str(self.value)

class FeatureSet:

	def __init__(self):
		self.featureDict = {}

	def __repr__(self):
		return str(self.featureDict)


	def initFeatureType(self, featureType):
		self.featureDict[featureType] = {}

	def addFeature(self, featureType, featureName, featureValue):
		self.featureDict[featureType][featureName] = Feature(featureName, featureValue)

	def updateFeature(self, featureType, featureName, increment, operation="sum"):
		if operation == "sum":
			self.featureDict[featureType][featureName].value += increment
		elif operation == "division":
			self.featureDict[featureType][featureName].value /= increment
		else:
			raise ValueError("Incorrect Operation")

	def getFeatureNames(self, featuresSelected=None):
		featureNames = []
		
		if featuresSelected is None:
			featuresSelected = self.featureDict.keys()
		
		for featType in featuresSelected:
			featureNames.expand(self.featureDict[featType].keys())

		return featureNames

	def getFeatureTypeNames(self,featuresSelected=None):
		featureTypeNames = []
		if featuresSelected is None:
			featuresSelected = self.featureDict.keys()

		for featType in featuresSelected:
			for featName in self.featureDict[featType].keys():
				featureTypeNames.append((featType,featName))

		return featureTypeNames

	def getFeatureVector(self, featureTypeNames):
		featureVector = []

		for featType, featName in featureTypeNames:
			featValue = self.featureDict[featType][featName].value
			featureVector.append(featValue)

		return featureVector