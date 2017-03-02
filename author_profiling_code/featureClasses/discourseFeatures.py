from __future__ import division
import codecs
from TreeLib.treeOperations import DiscourseTreeOperations
import os
import nltk
import utils

class DiscourseFeatures:

	def __init__(self,iC, modelName):	
		
		self.iC = iC
		self.type = "DiscourseFeatures"
		self.iC.initFeatureType(self.type)
		self.treeDict = {}
		self.allDeps = []
		self.modelName = modelName

	def compute_discourse_features(self):
		functionName = "compute_discourse_features"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		nPosts = len(self.iC.instances)
		nDone = 0
		for instance in self.iC.instances:
			discourseOut = instance.discourse
			iTree = DiscourseTreeOperations(discourseOut)
			sentences = instance.sentences
			nsents =  len(sentences)

			self.get_shape_features(iTree, nsents, instance)
			self.get_discourse_relation_usage(iTree, nsents, instance)
			nDone +=1
			print "processed " + str(nDone) + " of " + str(nPosts)
		
		self.adjust_features()
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,self.allDeps,self.iC, self.type)


	def get_shape_features(self, iTree, nsents, instance):
		instance.addFeature(self.type, "DISCSHAPE_discwidth", iTree.get_max_width() / nsents)
		instance.addFeature(self.type, "DISCSHAPE_discdepth", iTree.get_max_depth() / nsents)
		instance.addFeature(self.type, "DISCSHAPE_discramFactor", iTree.get_ramification_factor() / nsents)


	def get_discourse_relation_usage(self, iTree, nsents, instance):
		relFreq,_ = iTree.search_deps_frequency()
		for rel, freq in relFreq.iteritems():	
			if "DISCREL_"+rel not in instance.featureSet.featureDict["DiscourseFeatures"]:
				instance.addFeature(self.type, "DISCREL_"+rel, 0.0)

			instance.updateFeature(self.type, "DISCREL_"+rel, freq / nsents)

			if "DISCREL_"+rel not in self.allDeps:
				self.allDeps.append("DISCREL_"+rel)

	def adjust_features(self):
		for instance in self.iC.instances:
			for featName in self.allDeps:
				if featName not in instance.featureSet.featureDict["DiscourseFeatures"]:
					instance.addFeature(self.type, featName, 0.0)
