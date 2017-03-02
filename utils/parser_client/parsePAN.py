# -*- coding: utf-8 -*-

import transition_client as tc
import json
import os
import urllib2
import nltk
import io
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')			

def clean(sentence):
	sentence = sentence.replace("\r\n"," ")
	sentence = sentence.replace(u'é',"e")
	sentence = sentence.replace(u'á',"a")
	sentence = sentence.replace(u'í',"i")
	sentence = sentence.replace(u'ó',"o")
	sentence = sentence.replace(u'ú',"u")
	sentence = sentence.replace(u'à',"a")
	sentence = sentence.replace(u'è',"e")
	sentence = sentence.replace(u'ì',"i")
	sentence = sentence.replace(u'ò',"o")
	sentence = sentence.replace(u'ù',"u")

	sentence = sentence.replace(u'É',"E")
	sentence = sentence.replace(u'Á',"A")
	sentence = sentence.replace(u'Í',"I")
	sentence = sentence.replace(u'Ú',"U")
	sentence = sentence.replace(u'Ó',"O")

	sentence = sentence.replace(u'È',"E")
	sentence = sentence.replace(u'À',"A")
	sentence = sentence.replace(u'Ì',"I")
	sentence = sentence.replace(u'Ù',"U")
	sentence = sentence.replace(u'Ò',"O")

	sentence = sentence.replace(u'ô',"o")
	sentence = sentence.replace(u'â',"a")
	sentence = sentence.replace(u'î',"i")
	sentence = sentence.replace(u'Ã',"a")
	sentence = sentence.replace(u'©',"")
	sentence = sentence.replace(u'º',"")
	sentence = sentence.replace(u'ª',"")
	sentence = sentence.replace(u'†',"")
	sentence = sentence.replace(u'û',"u")
	sentence = sentence.replace(u'ê',"e")
	sentence = sentence.replace(u'Â',"A")
	sentence = sentence.replace(u'Ê',"E")
	sentence = sentence.replace(u'Î',"I")
	sentence = sentence.replace(u'Ô',"O")
	sentence = sentence.replace(u'Û',"U")
	sentence = sentence.replace(u'¢',"c")
	sentence = sentence.replace(u'±',"")
	sentence = sentence.replace(u'¶',"")
	sentence = sentence.replace(u'´',"'")
	sentence = sentence.replace(u'¦',"")
	sentence = sentence.replace(u'Ç',"C")
	sentence = sentence.replace(u'π',"pi")
	sentence = sentence.replace(u'ο',"o")
	sentence = sentence.replace(u'λ',"")
	sentence = sentence.replace(u'ἀ',"")
	sentence = sentence.replace(u'τ',"")
	sentence = sentence.replace(u'δ',"")

	sentence = sentence.replace(u'ë',"e")
	sentence = sentence.replace(u'ä',"a")
	sentence = sentence.replace(u'ï',"i")
	sentence = sentence.replace(u'ö',"o")
	sentence = sentence.replace(u'ü',"u")
	sentence = sentence.replace(u'—',"-")
	sentence = sentence.replace(u'“','"')
	sentence = sentence.replace(u'”','"')
	sentence = sentence.replace(u'ç','c')
	sentence = sentence.replace(u'ñ','n')
	sentence = sentence.replace(u'œ',"oe")
	sentence = sentence.replace(u'Œ',"OE")
	sentence = sentence.replace(u'æ',"ae")
	sentence = sentence.replace(u'Æ',"AE")
	sentence = sentence.replace(u'¨',"")
	sentence = sentence.replace(u'®',"r")
	sentence = sentence.replace(u'Å',"a")
	sentence = sentence.replace(u'¼',"")
	sentence = sentence.replace(u'£',"pound")
	sentence = sentence.replace(u'$',"dollar")
	sentence = sentence.replace(u'€',"euro")
	sentence = sentence.replace(u'»','"')
	sentence = sentence.replace(u'«','"')
	sentence = sentence.replace(u'¿',"")
	return sentence

def do_parse(path):
	iT = tc.TransitionClient(tc.EN_PARSER)

	if os.path.isfile(path+"_parsed"):
		print "Already processed"

	else:
		text = io.open(path,"r",encoding="utf-8").read()
		sentences = tokenizer.tokenize(text)

		for sentence in sentences:
			sentence = clean(sentence)

			try:
				output = str(iT.parse_text(sentence.encode("utf-8")))

			except urllib2.HTTPError as e:
				print e
				print sentence
				exit()

			with open(path+"_parsed","a") as fd:
				fd.write(output +"\n\n")



path = "/home/joan/Escritorio/Datasets/PANEssays/Test/"

i = 1
nelems = 599

while i < nelems:
	idProblem = "EE"
	if i < 10:
		idProblem += "00"
	elif i < 100:
		idProblem += "0"
	
	idProblem += str(i)

	if os.path.isdir(path+idProblem):
		pathKnown = path + idProblem + "/known0"
		j=1
		while j<7:
			pathKnownElem = pathKnown + str(j)+".txt"
			if os.path.isfile(pathKnownElem):
				do_parse(pathKnownElem)
			else:
				break
			j+=1

		pathUnknown = path + idProblem +"/unknown.txt"
		do_parse(pathUnknown)
			
		print "Processed "+idProblem

	i+=1