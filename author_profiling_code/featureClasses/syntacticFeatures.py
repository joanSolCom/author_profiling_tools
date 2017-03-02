from __future__ import division
import codecs
import numpy as np
from TreeLib.treeOperations import SyntacticTreeOperations
import os
import utils

class SyntacticFeatures:

	adverbialRelations = ["ADV","TMP","LOC","DIR","MNR","PRP","EXT"]
	modifierRelations = ["NMOD","PMOD","AMOD"]

	verbTags = ["VB","VBD","VBG","VBN","VBP","VBZ", "MD"]
	nounTags = ["NN","NNS","NNP","NNPS"]
	adverbTags = ["RB","RBR","RBS","WRB"]
	adjectiveTags = ["JJ","JJR","JJS"]
	pronounTags = ["PRP","PRP$","WP","WP$"]
	determinerTags = ["DT","PDT","WDT"]
	conjunctionTags = ["CC","IN"]

	superlatives = ["JJS","RBS"]
	comparatives = ["JJR","RBR"]
	
	pastVerbs = ["VBD","VBN"]
	presentVerbs = ["VBG","VBP","VBZ"]

	def __init__(self,iC, modelName):	
		
		self.iC = iC
		self.type = "SyntacticFeatures"
		self.iC.initFeatureType(self.type)
		self.allRelationsPos = []
		self.modelName = modelName


	def compute_syntactic_features(self):
		functionName = "compute_syntactic_features"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		nPosts = len(self.iC.instances)
		nProcessed = 0
		print "Building Syntactic Trees"
		for instance in self.iC.instances:
			conllSents = instance.conll.split("\n\n")
			iTrees = []
			conllSents = conllSents[:-1]
			for conllSent in conllSents:
				try:
					iTree = SyntacticTreeOperations(conllSent)
					iTrees.append(iTree)
				except ValueError as e:
					print e
					continue

			self.get_relation_usage(iTrees, instance)
			self.get_relationgroup_usage(iTrees, instance)
			self.get_pos_usage(iTrees, instance)
			self.get_posgroup_usage(iTrees, instance)
			
			self.get_shape_features(iTrees, instance)
			self.get_subcoord_features(iTrees, instance)
			self.get_verb_features(iTrees, instance)
			nProcessed +=1
			print "processed "+str(nProcessed) + " of " + str(nPosts)

		self.adjust_features()
		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,self.allRelationsPos,self.iC, self.type)

	#to be used after get_relation_usage and get_pos_usage
	def adjust_features(self):
		for instance in self.iC.instances:
			for featName in self.allRelationsPos:
				if featName not in instance.featureSet.featureDict["SyntacticFeatures"]:
					instance.addFeature(self.type, featName, 0.0)

	def get_relation_usage(self, iTrees, instance):
		nTrees = len(iTrees)
		for iTree in iTrees:
			depFreq,_ = iTree.search_deps_frequency()
			for dep, freq in depFreq.iteritems():	
				if "SYNDEP_"+ dep not in instance.featureSet.featureDict["SyntacticFeatures"].keys():
					instance.addFeature(self.type, "SYNDEP_"+dep, 0.0)
				
				instance.updateFeature(self.type, "SYNDEP_"+dep, freq / nTrees)
				
				if "SYNDEP_"+dep not in self.allRelationsPos:
					self.allRelationsPos.append("SYNDEP_" + dep)

	def get_relationgroup_usage(self,iTrees, instance):
		nTrees = len(iTrees)
		instance.addFeature(self.type, "SYNDEP_modifierRelations", 0.0)
		instance.addFeature(self.type, "SYNDEP_adverbialRelations", 0.0)

		for iTree in iTrees:
			depFreq, total = iTree.search_deps_frequency(self.adverbialRelations)
			instance.updateFeature(self.type, "SYNDEP_adverbialRelations", total / nTrees)

			depFreq, total = iTree.search_deps_frequency(self.modifierRelations)
			instance.updateFeature(self.type, "SYNDEP_modifierRelations", total / nTrees)


	def get_posgroup_usage(self, iTrees, instance):
		nTrees = len(iTrees)
		instance.addFeature(self.type, "SYNPOS_verbTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_nounTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_adverbTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_adjectiveTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_pronounTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_determinerTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_conjunctionTags", 0.0)
		instance.addFeature(self.type, "SYNPOS_superlatives", 0.0)
		instance.addFeature(self.type, "SYNPOS_comparatives", 0.0)
		instance.addFeature(self.type, "SYNPOS_pastVerbs", 0.0)
		instance.addFeature(self.type, "SYNPOS_presentVerbs", 0.0)


		for iTree in iTrees:
			depFreq, total = iTree.search_pos_frequency(self.verbTags)
			instance.updateFeature(self.type, "SYNPOS_verbTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.nounTags)
			instance.updateFeature(self.type, "SYNPOS_nounTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.adverbTags)
			instance.updateFeature(self.type, "SYNPOS_adverbTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.adjectiveTags)
			instance.updateFeature(self.type, "SYNPOS_adjectiveTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.pronounTags)
			instance.updateFeature(self.type, "SYNPOS_pronounTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.determinerTags)
			instance.updateFeature(self.type, "SYNPOS_determinerTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.conjunctionTags)
			instance.updateFeature(self.type, "SYNPOS_conjunctionTags", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.superlatives)
			instance.updateFeature(self.type, "SYNPOS_superlatives", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.comparatives)
			instance.updateFeature(self.type, "SYNPOS_comparatives", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.pastVerbs)
			instance.updateFeature(self.type, "SYNPOS_pastVerbs", total / nTrees)

			depFreq, total = iTree.search_pos_frequency(self.presentVerbs)
			instance.updateFeature(self.type, "SYNPOS_presentVerbs", total / nTrees)


	def get_pos_usage(self,iTrees, instance):
		nTrees = len(iTrees)
		for iTree in iTrees:
			posFreq, _ = iTree.search_pos_frequency()
			for pos, freq in posFreq.iteritems():
				if "SYNPOS_"+pos not in instance.featureSet.featureDict["SyntacticFeatures"]:
					instance.addFeature(self.type, "SYNPOS_"+pos, 0.0)

				instance.updateFeature(self.type, "SYNPOS_"+pos, freq / nTrees)
				
				if "SYNPOS_"+pos not in self.allRelationsPos:
					self.allRelationsPos.append("SYNPOS_"+pos)

	def get_shape_features(self,iTrees, instance):
		nTrees = len(iTrees)
		instance.addFeature(self.type, "SYNSHAPE_width", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_depth", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_ramFactor", 0.0)

		for iTree in iTrees:
			ramFact = iTree.get_ramification_factor()
			width = iTree.get_max_width()
			depth = iTree.get_max_depth()
			instance.updateFeature(self.type, "SYNSHAPE_width", width / nTrees)
			instance.updateFeature(self.type, "SYNSHAPE_depth", depth / nTrees)
			instance.updateFeature(self.type, "SYNSHAPE_ramFactor", ramFact / nTrees)

	def get_subcoord_features(self, iTrees, instance):
		nSubs = 0
		nCoords = 0

		instance.addFeature(self.type, "SYNSHAPE_subDepth", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_subWidth", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_subRamFact", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_subLevel", 0.0)

		instance.addFeature(self.type, "SYNSHAPE_coordDepth", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_coordWidth", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_coordRamFact", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_coordLevel", 0.0)


		for iTree in iTrees:
			subFreq, numS =  iTree.search_deps_frequency(["SUB"])
			if subFreq:
				nSubs += numS

			coordFreq, numC =  iTree.search_deps_frequency(["COORD"])
			if coordFreq:
				nCoords += numC

			widthDepth = iTree.get_relation_width_depth("SUB")
			if widthDepth:
				incrementW = sum([pair[0] for pair in widthDepth]) / len(widthDepth)
				incrementD = sum([pair[1] for pair in widthDepth]) / len(widthDepth)

				instance.updateFeature(self.type, "SYNSHAPE_subWidth", incrementW)
				instance.updateFeature(self.type, "SYNSHAPE_subDepth", incrementD)

			ramFactors = iTree.get_relation_ramification_factor("SUB")
			if ramFactors:
				incrementR = np.sum(np.array(ramFactors)) / len(ramFactors)
				instance.updateFeature(self.type, "SYNSHAPE_subRamFact", incrementR)

			levels = iTree.get_relation_depth_level("SUB")
			if levels:
				incrementSL = np.sum(np.array(levels)) / len(levels)
				instance.updateFeature(self.type, "SYNSHAPE_subLevel", incrementSL)

			widthDepth = iTree.get_relation_width_depth("COORD")
			if widthDepth:
				incrementCW = sum([pair[0] for pair in widthDepth]) / len(widthDepth)
				incrementCD = sum([pair[1] for pair in widthDepth]) / len(widthDepth)

				instance.updateFeature(self.type, "SYNSHAPE_coordWidth", incrementCW)
				instance.updateFeature(self.type, "SYNSHAPE_coordDepth", incrementCD)

			ramFactors = iTree.get_relation_ramification_factor("COORD")
			if ramFactors:
				incrementCR = np.sum(np.array(ramFactors)) / len(ramFactors)
				instance.updateFeature(self.type, "SYNSHAPE_coordRamFact", incrementCR)

			levels = iTree.get_relation_depth_level("COORD")
			if levels:
				incrementCL = np.sum(np.array(levels)) / len(levels)
				instance.updateFeature(self.type, "SYNSHAPE_coordLevel", incrementCL)

		if nSubs > 0:
			instance.updateFeature(self.type, "SYNSHAPE_subDepth", nSubs, "division")
			instance.updateFeature(self.type, "SYNSHAPE_subWidth", nSubs, "division")
			instance.updateFeature(self.type, "SYNSHAPE_subRamFact", nSubs, "division")
			instance.updateFeature(self.type, "SYNSHAPE_subLevel", nSubs, "division")

		if nCoords > 0:
			instance.updateFeature(self.type, "SYNSHAPE_coordDepth", nCoords, "division")
			instance.updateFeature(self.type, "SYNSHAPE_coordWidth", nCoords, "division")
			instance.updateFeature(self.type, "SYNSHAPE_coordRamFact", nCoords, "division")
			instance.updateFeature(self.type, "SYNSHAPE_coordLevel", nCoords, "division")

	def get_verb_features(self, iTrees, instance):
		nTrees = len(iTrees)
		instance.addFeature(self.type, "SYNSHAPE_composedVerbRatio", 0.0)
		instance.addFeature(self.type, "SYNSHAPE_modalRatio", 0.0)

		for iTree in iTrees:
			composedVerbRatio = iTree.get_composed_verb_ratio()
			modalRatio = iTree.get_modal_ratio()
			instance.updateFeature(self.type, "SYNSHAPE_composedVerbRatio", composedVerbRatio / nTrees)
			instance.updateFeature(self.type, "SYNSHAPE_modalRatio", modalRatio / nTrees)
