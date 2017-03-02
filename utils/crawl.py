from lxml import etree
import os
import re
from lxml import html
import codecs
import requests

baseUrl = 'https://api.voat.co/api/v1/v/coontown&Voat-ApiKey=APIKEY'
pathOut = "/home/joan/Escritorio/Datasets/GayBlogs/clean/"

apiKey






'''
while nxt:
	page = requests.get(url)
	tree = html.fromstring(page.content)
	nxt = tree.xpath("//div[@id='mw-pages']/a[text()='next page']/@href")
	cardUrlsList = tree.xpath("//div[@class='mw-category-group']/ul/li/a/@href")
	for cardUrl in cardUrlsList:
		cardUrls.append(baseUrl+cardUrl)
	
	if nxt:
		urlNext = baseUrl + nxt[0]
		url = urlNext


for cardUrl in cardUrls:
	page = requests.get(cardUrl)
	tree = html.fromstring(page.content)
	textCard = tree.xpath("//div[@id='mw-content-text']/p//text() | //div[@id='mw-content-text']/dl//text()")
	cardName = tree.xpath("//h1[@id='firstHeading']//text()")[0]
	try:
		outFile = codecs.open("/home/joan/Escritorio/Datasets/heartPedia/cards/"+cardName,"w",encoding="utf-8")
	except IOError:
		print "Error with card"
		print cardName
		print cardUrl
		continue

	acumText = ""
	for textPiece in textCard:
		acumText+=textPiece
		if "\n" in acumText:
			outFile.write(acumText)
			acumText = ""

	outFile.close()

'''
'''
counter = 0
for hrefJohn in hrefsJohn:
	page = requests.get(hrefJohn)
	tree = html.fromstring(page.content)
	paragraphs = tree.xpath("//div[@class='format_text entry-content']/p//text()")
	out = open(pathOut+str(counter)+"_male_johnQuiggin_notgay.txt", "w")
	for paragraph in paragraphs:
		out.write(paragraph.encode("utf-8"))

	out.close()
	
	counter+=1
	if counter == 500:
		break
	print "John written " + str(counter)

counter=0
'''
'''
counter = 0
for hrefKieran in hrefsKieran:
	page = requests.get(hrefKieran)
	tree = html.fromstring(page.content)
	paragraphs = tree.xpath("//div[@class='format_text entry-content']/p//text()")
	out = open(pathOut+str(counter)+"_male_kieranHealy_notgay.txt", "w")
	for paragraph in paragraphs:
		out.write(paragraph.encode("utf-8"))

	out.close()
	
	counter+=1
	if counter == 500:
		break

	print "Kieran written " + str(counter)

'''
'''
while idPage < 40:
	page = requests.get(url + str(idPage))
	tree = html.fromstring(page.content)

	hrefs = tree.xpath("//div[@class='right-col']/h2/a/@href")

	for href in hrefs:
		page = requests.get("https://crooksandliars.com"+href)
		tree = html.fromstring(page.content)

		paragraphs = tree.xpath("//div[@class='content']/p//text()")

		out = open(pathOut+str(counter)+labels, "w")
		for paragraph in paragraphs:
			out.write(paragraph.encode("utf-8"))

		out.close()
		
		counter+=1
		print "written " + str(counter)
	
	idPage+=1


'''
'''
for hrefSum in hrefSummaries:
	page = requests.get("http://www.goodasyou.org"+hrefSum)
	tree = html.fromstring(page.content)
	fullArticle = tree.xpath('//p[@style="text-align:center;"]/a/@href')[0]
		
	page = requests.get(fullArticle)
	tree = html.fromstring(page.content)
	paragraphs = tree.xpath('//div[@id="center"]/div[@class="content"]/p[count(@*)=0]/text()')
	out = open(pathOut+str(counter)+labels, "w")
	for paragraph in paragraphs:
		out.write(paragraph.encode("utf-8"))

	out.close()
	counter+=1
	print "written " + str(counter) + " of " + str(len(hrefSummaries))
'''

