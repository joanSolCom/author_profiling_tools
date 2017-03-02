# -*- coding: utf-8 -*-
import instanceManager
from instanceManager import InstanceCollection
import cPickle as pickle
from featureClasses.characterBasedFeatures import CharacterBasedFeatures
from featureClasses.wordBasedFeatures import WordBasedFeatures
from featureClasses.sentenceBasedFeatures import SentenceBasedFeatures
from featureClasses.dictionaryBasedFeatures import DictionaryBasedFeatures
from featureClasses.syntacticFeatures import SyntacticFeatures
from featureClasses.discourseFeatures import DiscourseFeatures
from featureClasses.lexicalFeatures import LexicalFeatures
from machineLearning.classify import SupervisedLearning

def save_model(filename, iC):
	with open(filename,'wb') as fp:
		pickle.dump(iC,fp)

def load_model(filename):
	iC = None
	try:
		with open(filename,'rb') as fp:
			print "Loading model..."
			iC = pickle.load(fp)
	except IOError:
		print "Model Not Found"
	return iC

def compute_features(paths, featureGroups, modelName, labelPosition, selectedLabels = None):
	print "Creating Instance Collection"
	iC = instanceManager.createInstanceCollection(paths, labelPosition, "_" ,selectedLabels)
	
	if "CharacterBasedFeatures" in featureGroups:	
		print "Character based"
		iChar = CharacterBasedFeatures(iC,modelName)
		iChar.get_uppers()
		iChar.get_numbers()
		iChar.get_symbols([","],"commas")
		iChar.get_symbols(["."],"dots")
		iChar.get_symbols(['?',"¿"],"questions")
		iChar.get_symbols(['!','¡'],"exclamations")
		iChar.get_symbols([":"],"colons")
		iChar.get_symbols([";"],"semicolons")
		iChar.get_symbols(['"',"'","”","“", "’"],"quotations")
		iChar.get_symbols(["—","-","_"],"hyphens")
		iChar.get_symbols(["(",")"],"parenthesis")
		iChar.get_in_parenthesis_stats()

	if "WordBasedFeatures" in featureGroups:
		print "Word based"
		iWord = WordBasedFeatures(iC,modelName)
		iWord.get_twothree_words()
		iWord.get_word_stdandrange()
		iWord.get_chars_per_word()
		iWord.get_vocabulary_richness()
		iWord.get_stopwords()
		iWord.get_acronyms()
		iWord.get_firstperson_pronouns()
		iWord.get_proper_nouns()

	if "SentenceBasedFeatures" in featureGroups:
		print "Sentence based"
		iSent = SentenceBasedFeatures(iC,modelName)
		iSent.get_wordsPerSentence_stdandrange()

	if "DictionaryBasedFeatures" in featureGroups:
		print "Dictionary based -> ojo que tarda un ratete"
		iDict = DictionaryBasedFeatures(iC,modelName)
		iDict.get_discourse_markers()
		iDict.get_dict_count()
		iDict.get_interjections()
		iDict.get_mean_mood()

	if "SyntacticFeatures" in featureGroups:
		print "Syntactic Features"
		iSyntactic = SyntacticFeatures(iC,modelName)
		iSyntactic.compute_syntactic_features()

	if "DiscourseFeatures" in featureGroups:
		print "Discourse Features"
		iDiscourse = DiscourseFeatures(iC,modelName)
		iDiscourse.compute_discourse_features()

	if "LexicalFeatures" in featureGroups:
		print "Lexical Features"
		iLexical = LexicalFeatures(iC, modelName)
		iLexical.generate_bow_features(500)
	
	return iC

def classify(iC, path, classifier = "SVM", save=False):
	iClassify = SupervisedLearning(iC)
	if classifier == "SVM":
		clf = iClassify.SVM()
	elif classifier == "RandomForests":
		clf = iClassify.RandomForests()
	else:
		clf = iClassify.SVM()

	if save:
		iClassify.save_model(clf,path)
	
	iClassify.cross_validation(clf)

modelName = "PUT A NAME HERE IT IS NOT VERY RELEVANT"
paths = {}
paths["clean"] = "PATH OF RAW FILES"
paths["discParsed"] = "PATH OF DICOURSE PROCESSED FILES"
paths["synParsed"] = "PATH OF SYNTACTIC PROCESSED FILES"

featureGroups = ["SyntacticFeatures", "CharacterBasedFeatures", "WordBasedFeatures", "SentenceBasedFeatures", "SentenceBasedFeatures", "DictionaryBasedFeatures", "LexicalFeatures"]

suffix = "_".join(featureGroups)
pathArff = "PATH WHERE YOU WANT YOUR WEKA FILE"

labelPosition = #POSITION OF YOUR LABEL IN THE FILE NAME
labeling = "NAME OF YOUR LABELING"
print modelName
print featureGroups
print labeling

iC = compute_features(paths, featureGroups, modelName, labelPosition)
print "to Arff"
iC.toArff(pathArff, modelName+labeling+"_"+suffix+".arff")
