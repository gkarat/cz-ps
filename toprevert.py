#!/usr/bin/python3
# coding=windows-1250

"""
Parses .html file to .prevert format

"""

import re
from lxml import etree


"""
<speech ID="http://www.vlada.cz/cz/vlada/premier/" FirstName="vlády" 
Surname="ČR" Url="<_sre.SRE_Match object; span=(9, 46), match='http://www.vlada.cz/cz/vlada/premier/'>" Function="Předseda">
"""

def personInfo(p):							# personInfo return value consists of [ROLE, FIRSTNAME, LASTNAME]
	if p[0:2] == "<b":
		info_block = re.search("(?<=u>).*(?=</u>)", p).group(0)
	else:
		info_block = re.search("(?<=>).*(?=</a>)", p).group(0)
	if info_block:
		if info_block.startswith("Poslan"):
			return info_block.split(" ", 2)
		else:
			return info_block.rsplit(" ", 2)


def print_speech_paragraph(fout, p):
	"""
	Writes ID of every new speech
	"""
	fout.write("<speech ID=\"")
	
	id_ = re.search("(?<=id=).*(?=\">)", p)
	href_ = None
	if not id_:													# person might doesn't have an id
		href_ = re.search("(?<=href=\").*(?=\">)", p)
		if href_:																# but it can have an own web-site (e.g. premier)
			if href_.group(0).endswith("/"):
				href_last = href_.group(0).split('/')[-2]
			else:
				href_last = href_.group(0).split('/')[-1]
			if href_last == "vlada":
				fout.write("")
			else:
				fout.write(href_last)
		else:												# otherwise leave ID field empty
			fout.write("")
	else:
		fout.write(id_.group(0))

	person_info = personInfo(p)

	fout.write("\" FirstName=\"%s\" Surname=\"%s\" " % (person_info[1], person_info[2]))

	if href_:
		url_ = href_.group(0)		# when a person has its own website
	else:
		if id_:			# if he has own page on www.psp.cz
			url_ = "https://www.psp.cz/" + re.search("(?<=href=\"/).*(?=\">)", p).group(0)
		else:			# if has no information about website TODO?
			url_ = ""

	fout.write("Url=\"%s\" Function=\"%s\">" % (url_, person_info[0]))
	fout.write("\n")


def print_paragraph(fout, p):
	"""
	Writes every single paragraph's text
	"""
	p = re.sub("&nbsp;", " ", p)		# replacing &nbsp; characters with whitespace
	fout.write("<p>\n")
	if p[0] == '<':
		fout.write(p.split(">: ")[-1] + "\n")
	else:
		fout.write(p + "\n")
	fout.write("</p>\n")


def to_prevert(filepath, fout):
	with open(filepath, encoding = "windows-1250") as protocol_file:
		content = protocol_file.read()

	new_peson = False
	
	for paragraph in re.findall('(?<=justify\">).*(?=</p>)', content):
		
		if paragraph == "&nbsp;":		# skip paragraphs without any meaningful text
			continue
		if paragraph[0] == '<':							# if paragraph belongs to the another person
			if new_peson:
				fout.write("</speech>\n")
			new_peson = True
			print_speech_paragraph(fout, paragraph)
		elif not new_peson:
			continue
		print_paragraph(fout, paragraph)
	fout.write("</speech>\n")
