#!/usr/bin/env python
import scraperwiki
import lxml.etree
import lxml.html
import requests

#get list of pdf urls for detention stats

urlList = []
mainPage = requests.get('https://www.border.gov.au/about/reports-publications/research-statistics/statistics/live-in-australia/immigration-detention').content
mainPageDom = lxml.html.fromstring(mainPage)

urlList2 = ['https://www.border.gov.au/ReportsandPublications/Documents/statistics/immigration-detention-statistics-feb2014.pdf']

for url in mainPageDom.cssselect('.ym-gbox-left a'):
	if url.attrib['href'] != "/":
		urlList.append("https://www.border.gov.au" + url.attrib['href'])

#function to get text elements 

def gettext_with_bi_tags(el):
	res = []
	if el.text:
		res.append(el.text)
	for lel in el:
		res.append("<%s>" % lel.tag)
		res.append(gettext_with_bi_tags(lel))
		res.append("</%s>" % lel.tag)
		if el.tail:
			res.append(el.tail)
	return "".join(res)

def cleanString(s):
	return s.replace("<b>","").replace("</b>","").replace('\n', ' ').lower().replace(u"\u00A0", " ").strip()

#go through the list of urls

def getStatsPage(pages):
	for pageNo, page in enumerate(pages):
		for el in list(page):
			#print gettext_with_bi_tags(el)
			elText = cleanString(gettext_with_bi_tags(el))
			#print elText
			if "place of immigration detention" in elText:
				statsPage = pageNo
	
	return statsPage			


for url in urlList:
	print "getting " + url
	pdfData = requests.get(url).content
	xmlData = scraperwiki.pdftoxml(pdfData)
	parser = lxml.etree.XMLParser(recover=True)
	root = lxml.etree.XML(xmlData, parser)
	pages = list(root)
	statsPage = getStatsPage(pages)
	for el in pages[statsPage]:
		print el.attrib, gettext_with_bi_tags(el)