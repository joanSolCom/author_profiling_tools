#AUTHOR PROFILING TOOLS

This is the code required to extract Juan Soler-Company's features from text and perform author profiling/identification.

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