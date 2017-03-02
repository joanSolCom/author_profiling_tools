from lxml import etree
import os
import re
from lxml import html
import codecs

path = "/home/joan/Escritorio/Datasets/PAN11Author/LargeValid.xml"

raw = open(path, "r").read()

#raw = raw.replace("&","and")

'''tree = etree.parse(raw)

#out = codecs.open(pathOut+fpath,"w", encoding="utf-8")

r = tree.xpath("/training/text/author/body//text()")
auth = tree.xpath("/training/text/author/@id")
for idText, text in enumerate(r):
	print text, auth[idText]
	exit()

'''
#out.close()

#<text file="LargeValid//a1001.xml">
'''
<text file="LargeValid//a1.xml">
 <author id="904579"/>
</text>
'''

def getAuthor(idAuth):
	groundTruth = open("/home/joan/Escritorio/Datasets/PAN11Author/GroundTruthLargeValid.xml","r").read()
	authorId = re.findall(r"file=\""+idAuth+'"'+">\n <author id="+'"'+r"(.*?)\"/>", groundTruth, re.DOTALL)
	return authorId[0]

ids = re.findall(r"file=\"(.*)\"",raw)
texts = re.findall(r"<body>(.*?)</body>",raw,re.DOTALL)

for idx,author in enumerate(ids):
	text = texts[idx]
	text = text.replace("<NAME/>","NAME")
	text = text.replace("<EMAIL/>","EMAIL")
	idAuth = ids[idx]
	author = getAuthor(idAuth)
	
	fd = open("/home/joan/Escritorio/Datasets/PAN11Author/LargeTest/clean/"+str(idx)+"_"+author,"w")
	fd.write(text)
	fd.close()
	

