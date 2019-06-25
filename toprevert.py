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
			fout.write(re.search("(?<=href=\").*(?=\">)", p).group(0))
		else:												# otherwise leave ID field empty
			fout.write("")
	else:
		fout.write(id_.group(0))

	if p[0:2] == "<b":
		info_name = re.search("(?<=u>).*(?=</u>)", p).group(0).rsplit(" ", 2)
	else:
		info_name = re.search("(?<=>).*(?=</a>)", p).group(0).rsplit(" ", 2)				# info_name consists of [ROLE, FIRSTNAME, LASTNAME]

	fout.write("\" FirstName=\"%s\" Surname=\"%s\" " % (info_name[1], info_name[2]))

	if href_:
		url_ = href_.group(0)		# when a person has its own website
	else:
		if id_:			# if he has own page on www.psp.cz
			url_ = "https://www.psp.cz/" + re.search("(?<=href=\"/).*(?=\">)", p).group(0)
		else:			# if has no information about website TODO?
			url_ = ""

	fout.write("Url=\"%s\" Function=\"%s\">" % (url_, info_name[0]))
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
