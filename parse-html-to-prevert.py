#!/usr/bin/python3
import sys
import re
from bs4 import BeautifulSoup


def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

"""
<p align="justify"><a href="/sqw/detail.sqw?id=5462">Pøedseda PSP Jan Hamáèek</a>: Dìkuji. Vážený pane místopøedsedo, 
dámy a pánové, vážená vládo, já bych nevystupoval, kdyby moje jméno nepadlo z&nbsp;úst jednoho z&nbsp;øeèníkù. 
A když už tedy to slovo mám, tak to vezmu trošku zeširoka. </p>

<speech ID="401" FirstName="Miroslava" SecondaryRole="poslanec" StenographerTitle="Řeč předsedající Miroslavy Němcové" Surname="Němcová" 
TitleAfter="" TitleBefore="" Url="http://www.psp.cz/sqw/detail.sqw?id=401" Function="Předsedající" Continue="False">
"""

def print_speech_paragraph(fout, p):
	### print ID
	fout.write("<speech ID=\"")
	fout.write(p.a['href'].split("id=")[-1])
	
	### info_name = [ROLE, FIRSTNAME, LASTNAME]
	info_name = p.find('a').text.rsplit(' ', 2)
	fout.write("\" FirstName=\"%s\" Surname=\"%s\" " % (info_name[1], info_name[2]))
	fout.write("Url=\"%s\" Function=\"%s\">" % ("https://www.psp.cz/" + p.a['href'], info_name[0]))
	fout.write("\n")


def print_paragraph(fout, p):
	space = " " * 10
	fout.write(space)
	fout.write("<p>\n")
	fout.write(space + "  " + p.text + "\n")
	fout.write(space)
	fout.write("</p>\n")


if __name__ == '__main__':
	#file_path = sys.argv[1]
	filename = "test.htm"
	with open(filename, encoding = "ISO-8859-1") as file:
		content = file.read()

	### odstraneni nepotrebnych radku
	content = content.split("\n", 16)[16].rsplit("\n", 4)[0]

	fout = open(filename.split('.')[0] + ".prevert", "w")
	soup = BeautifulSoup(content, "lxml")
	for paragraph in soup.find_all('p'):
		### if paragraph belongs to the another person
		if paragraph.find('a'):
			print_speech_paragraph(fout, paragraph)
		### write the content in .prevert format
		print_paragraph(fout, paragraph)

	fout.close()
