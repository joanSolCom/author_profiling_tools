#AUTHOR PROFILING TOOLS

This is the code required to extract Juan Soler-Company's features from text and perform author profiling/identification.

If this code is used, please cite the following paper:

@inproceedings{solerEACL17,

    title={{On the Relevance of Syntactic and Discourse Features for Author Profiling and Identification}},

    author={Soler-Company, Juan and Wanner, Leo},

    booktitle={{15th Conference of the European Chapter of the Association for Computational Linguistics (EACL)}},

    year={2017},

    pages={681--687}

}


The repository has the following structure:

utils/ 

This contains code to perform different tasks such as web crawling, or dependency parsing.

baselines/

This folder contains code to compute different alternative sets of features usually used as baselines.

author_profiling_code/

Here is where the magic happens

HOW TOs

How do I syntactically parse a text?

Go to utils/parse_client/parse.py
Change these lines:

out_processed = "INTRODUCE THE OUTPUT PATH"

out_clean = "INTRODUCE RAW TEXT PATH"

The first path is where you want your parsed files to be stored (needs to exist before executing)
The second one is where you have the files of your corpus (the clean txt files)

Execute the parse.py and the output files will be stored in the path you specified. This needs to be done before executing the author profiling code. In the out_processed folder you will have files named the same way as the original raw files in conll format (the standard output format for parsing). The program calls an external web service, so all the work is done in the TALNs servers.

How do I discourse parse a text?

Ok, we switch now to Java. To discourse parse a text, go to utils/ROFL/ (i created this files in a time i was really bored) and import this project using eclipse ee (import it as a maven project or just create a new maven project, copy the contents of the pom in the created pom and copy the files, but probably easier to import it). The code is in App.java, and the key part is that the discourse parser is added via maven (file pom.xml has the proper information). You only need to change the lines where you have to specify your input path and your desired output path. This uses around 3-4Gb of ram, but you should be able to run it locally without issues. 

After having the files that correspond to the syntactic and discourse parsers, we can move on to the main code.

To use my code, your data should have this structure:

dataset_name/

.../dataset_name/folder_with_raw_files/ -> this is where the txt files of your corpus are stored
.../dataset_name/folder_with_synParsed_files/ -> contains the conll files with the output of the dependency parser
.../dataset_name/folder_with_discParsed_files/ -> contains the discourse files

the names of the files in the three folders need to be coherent, so if you have myfile1.txt in raw, that filename should be in the other two folders with the conll and disc files.

The format of the files should be the following:

id_label

The id is usually a numeric identifier and the label should be for example, the native language of the writer of that text, so you should have filenames that look like this:

1_japanese

2_chinese

3_japanese

4_korean

After generating both discourse and syntactic parses and having the file name and file structure as I mentioned before, we can execute my code.

The main file is located in author_profiling_code/main.py . In that file, you will have to edit a couple of things:

modelName = "PUT A NAME HERE IT IS NOT VERY RELEVANT"

paths = {}

paths["clean"] = "PATH OF RAW FILES"

paths["discParsed"] = "PATH OF DICOURSE PROCESSED FILES"

paths["synParsed"] = "PATH OF SYNTACTIC PROCESSED FILES"


featureGroups = ["SyntacticFeatures", "CharacterBasedFeatures", "WordBasedFeatures", "SentenceBasedFeatures", "SentenceBasedFeatures", "DictionaryBasedFeatures", "LexicalFeatures"]

suffix = "_".join(featureGroups)

pathArff = "PATH WHERE YOU WANT YOUR WEKA FILE"

labelPosition = #POSITION OF YOUR LABEL IN THE FILE NAME. IMPORTANT, if your files are 1_korean, you should put 1 here.

labeling = "NAME OF YOUR LABELING"

It is pretty self explanatory, but try to put absolute paths. By labeling I mean what kind of labels are there, in a nli problem, could be simply "native language" (it is not relevant). 
In the featureGroups array, you put the feature groups that you want to compute, right now, every possibility is in the array. As for lexical features, you can use the N most frequent words to classify, to indicate how many words to use, edit the following line: 

iLexical.generate_bow_features(500)

Right now it uses the 500 most common words. Probably would want to either remove the LexicalFeatures group in the array, or use a small amount of words changing that 500 by a smaller amount, such as 50.

The internal file structure in the author_profiling_code folder is as follows:

precalculated/ -> where computed files are stored, to not have to compute redundant feature values (if you think there is an error and want to recalculate them, go into precalculated/features and delete the files that correspond to the features that were computed).

machineLearning/ -> machine learning code, that uses sklearn algorithms, it can be ignored.

outputs/ -> where i usually save my weka files

TreeLib/ -> code to compute tree-related features

dicts/ -> dictionaries that are used by the dictionary-based features

featureClasses/ -> classes where the feature computations are.

After executing main.py, if there are no errors, an arff file will be located in the path you indicated. Then you can open it with the weka explorer and you can use the algorithms that are implemented in weka.

The best performing algorithms are usually LibSVM with a linear kernel after applying a filter which is called standardize.

==================
REQUIREMENTS

Python 2.7
	- numpy
	- scipy
	- sklearn
	- nltk (download every package available to nltk to make sure)

Java 7 (i believe that with 8 it works fine as well)
Weka (if LibSVM is not present, install the development version and add it with the package manager)
