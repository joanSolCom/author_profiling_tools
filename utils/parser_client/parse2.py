# -*- coding: utf-8 -*-

import transition_client as tc
import json
import os
import urllib2
import nltk
import codecs
import re

iT = tc.TransitionClient(tc.EN_PARSER)

out_processed = "PUT YOUR OUTPUT PATH HERE"
out_clean = "PUT YOUR RAW INPUT PATH HERE"

#out_processed = "/home/joan/Escritorio/Datasets/Mujerji/new_syn/"
#out_clean = "/home/joan/Escritorio/Datasets/Mujerji/new_clean/"

#out_clean = "/home/joan/Escritorio/Datasets/GayBlogs/clean/"
#out_processed = "/home/joan/Escritorio/Datasets/GayBlogs/synParsed/"

i = 0
listdir = os.listdir(out_clean)
size = len(listdir)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

for fname in listdir:
	if os.path.isfile(out_processed+fname):
		print "Already processed"

	else:
		print fname
		try:
			text = codecs.open(out_clean+fname,"r",encoding="utf-8").read()
		except UnicodeDecodeError:
			text = codecs.open(out_clean+fname,"r",encoding="latin1").read()

		sentences = tokenizer.tokenize(text)

		for sentence in sentences:
			try:
				sentence = emoji_pattern.sub(r'', sentence)
				output = str(iT.parse_text(sentence.encode("utf-8")))

			except urllib2.HTTPError as e:
				print e
				print sentence
				exit()

			with open(out_processed+fname,"a") as fd:
				fd.write(output +"\n\n")
		
		print "Processed "+str(i)+" of " + str(size)

	i+=1