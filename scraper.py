#!/usr/bin/env python
import scraperwiki
import lxml.etree
import lxml.html
import requests

#get list of pdf urls for detention stats

urlList = []
mainPage = requests.get('https://www.border.gov.au/about/reports-publications/research-statistics/statistics/live-in-australia/immigration-detention').content
mainPageDom = lxml.html.fromstring(mainPage)

urlList2 = ['https://www.border.gov.au/ReportsandPublications/Documents/statistics/immigration-detention-statistics-dec2014.pdf']

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
	data = {}
	print "getting " + url
	pdfData = requests.get(url).content
	xmlData = scraperwiki.pdftoxml(pdfData)
	parser = lxml.etree.XMLParser(recover=True)
	root = lxml.etree.XML(xmlData, parser)
	pages = list(root)
	statsPage = getStatsPage(pages)

	totalColumnPos = []

	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		# print elText
		# print el.attrib
		if elText == 'total':
			leftPos = el.attrib['left']
			totalIndex = i
			break
		if elText == 'women  children  total':
			leftPos = '592'
			totalIndex = i
			break	
	
	for i, el in enumerate(pages[statsPage]):		
		if (i > totalIndex) and (int(el.attrib['left']) < int(leftPos) + 20) and (int(el.attrib['left']) > int(leftPos) - 20):
			# print gettext_with_bi_tags(el)	
			totalColumnPos.append(i)

	#print totalColumnPos
	
	# for i in totalColumnPos:
	# 	print gettext_with_bi_tags(pages[statsPage][i])

	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("christmas island idc" in elText) or ("christmas island immigration detention" in elText) or ("island immigration detention" in elText):
			print "christmas island idc"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Christmas Island IDC'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break
	
	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("maribyrnong idc" in elText) or ("maribyrnong" in elText):
			print "maribyrnong idc"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Maribyrnong IDC'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break				


	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("perth idc" in elText) or ("perth immigration detention" in elText):
			print "Perth IDC"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Perth IDC'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break							
	
	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("villawood idc" in elText) or ("villawood immigration detention" in elText):
			print "Villawood IDC"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Villawood IDC'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break				

	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("yongah hill idc" in elText) or ("yongah hill immigration" in elText):
			print "Yongah Hill IDC"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Yongah Hill IDC'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break						

	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("curtin immigration detention centre" in elText) or ("curtin idc" in elText):
			print "Curtin IDC"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Curtin Immigration Detention Centre'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break				

	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if ("curtin immigration detention centre" in elText) or ("curtin idc" in elText):
			print "Curtin IDC"
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Curtin Immigration Detention Centre'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break	


	for i, el in enumerate(pages[statsPage]):
		elText = cleanString(gettext_with_bi_tags(el))
		if (elText == "total" or elText == "total facility" or elText == "total facility and apod") and (int(el.attrib['top']) > 500):

			print "Total onshore"
			# print el.attrib
			# print gettext_with_bi_tags(el)
			for total in totalColumnPos:
				if total > i:
					#print total
					data['Total onshore'] = cleanString(gettext_with_bi_tags(pages[statsPage][total]))
					break				

	print data


